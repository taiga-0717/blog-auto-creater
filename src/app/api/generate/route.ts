import { NextRequest, NextResponse } from 'next/server'
import Anthropic from '@anthropic-ai/sdk'
import { scrapeUrl, scrapeMultipleUrls } from '@/lib/scraper'
import { GenerateRequest } from '@/types'

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

// 毎回同じ内容にしてプロンプトキャッシュを効かせる（日時など可変値を入れないこと）
const SYSTEM_PROMPT = `あなたはプロのブログライターです。ユーザーが渡す情報をもとに、オリジナルのブログ記事を日本語で作成してください。

## 記事作成のルール
1. 「あなたのブログコンテンツ」から文体、トーン、語り口を学習し、同じスタイルで新しい記事を書いてください
2. コンテンツの内容を参考にしながら、独自の視点を加えた新しい記事を作成してください
3. 読者が最後まで読みたくなるような構成にしてください
4. 見出し（#, ##）を使って読みやすく整理してください
5. 使用禁止ワードが指定されている場合、それらは絶対に使用しないでください
6. 記事末尾の定型文が指定されている場合は、記事の最後に必ず追加してください
7. 出力は記事本文のみとしてください`

export async function POST(req: NextRequest) {
  try {
    const body: GenerateRequest = await req.json()
    const { blogIndexUrl, referenceLinks, ngWords, closingText, customInstruction } = body

    if (!blogIndexUrl) {
      return NextResponse.json({ success: false, error: 'ブログのURLを入力してください' }, { status: 400 })
    }

    if (!process.env.ANTHROPIC_API_KEY) {
      return NextResponse.json({ success: false, error: 'APIキーが設定されていません' }, { status: 500 })
    }

    // ブログコンテンツをスクレイピング
    const blogContent = await scrapeUrl(blogIndexUrl)

    // 参照リンクのスクレイピング（存在する場合）
    let referenceContents: string = ''
    if (referenceLinks && referenceLinks.length > 0) {
      const validLinks = referenceLinks.filter(link => link.trim())
      if (validLinks.length > 0) {
        const refs = await scrapeMultipleUrls(validLinks)
        referenceContents = refs.map((r, i) =>
          `【参照${i + 1}】${r.title}\nURL: ${r.url}\n内容:\n${r.content}`
        ).join('\n\n---\n\n')
      }
    }

    // NGワードの処理
    const ngWordsText = ngWords && ngWords.length > 0
      ? `\n\n## 使用禁止ワード\n以下の言葉は絶対に使用しないでください:\n${ngWords.map(w => `- ${w}`).join('\n')}`
      : ''

    // 定型文の処理
    const closingSection = closingText
      ? `\n\n## 記事末尾の定型文\n記事の最後に必ず以下の文章を追加してください:\n\n${closingText}`
      : ''

    // 参照コンテンツセクション
    const referenceSection = referenceContents
      ? `\n\n## 参照コンテンツ\n以下の参照情報も活用して記事を作成してください:\n\n${referenceContents}`
      : ''

    // カスタム指示
    const customSection = customInstruction
      ? `\n\n## 追加指示\n${customInstruction}`
      : ''

    // 変動部分（参照・NGワード・定型文・追加指示）は毎回変わるので、キャッシュ対象の後ろに置く
    const variableSections = `${referenceSection}${ngWordsText}${closingSection}${customSection}`.trim()

    // コスト最適化:
    // - claude-opus-5-5 は旧 claude-opus-4-5 より高性能かつ単価が安い（入力 $4 / 出力 $20 per 1M tokens）
    // - 固定の指示（system）と自分のブログ本文はプロンプトキャッシュに乗せ、同じブログで続けて生成する際の入力コストを約1/10にする
    // - effort は品質と思考トークン量のバランスが取れる medium を明示
    const response = await client.beta.messages.create({
      model: 'claude-opus-5-5',
      max_tokens: 16000,
      betas: ['server-side-fallback-2026-07-01'],
      // 安全分類器で拒否された場合はサーバー側で自動的に別モデルで再実行する
      fallbacks: 'default',
      output_config: { effort: 'medium' },
      system: [
        {
          type: 'text',
          text: SYSTEM_PROMPT,
          cache_control: { type: 'ephemeral' }
        }
      ],
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: `## あなたのブログコンテンツ（文体・スタイルの参考）\nタイトル: ${blogContent.title}\nURL: ${blogContent.url}\n\n内容:\n${blogContent.content}`,
              cache_control: { type: 'ephemeral' }
            },
            {
              type: 'text',
              text: `${variableSections ? variableSections + '\n\n' : ''}それでは、上記のスタイルに合わせたブログ記事を作成してください:`
            }
          ]
        }
      ]
    })

    if (response.stop_reason === 'refusal') {
      return NextResponse.json(
        { success: false, error: 'この内容では記事を生成できませんでした。参照リンクや追加指示を見直してください' },
        { status: 422 }
      )
    }

    const article = response.content
      .filter(block => block.type === 'text')
      .map(block => (block as { type: 'text'; text: string }).text)
      .join('\n')

    if (response.stop_reason === 'max_tokens') {
      console.warn('Generation hit max_tokens; article may be truncated')
    }

    return NextResponse.json({ success: true, article })
  } catch (error) {
    console.error('Generation error:', error)
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : '記事生成中にエラーが発生しました' },
      { status: 500 }
    )
  }
}
