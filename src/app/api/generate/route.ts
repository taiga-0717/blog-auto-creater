import { NextRequest, NextResponse } from 'next/server'
import Anthropic from '@anthropic-ai/sdk'
import { scrapeUrl, scrapeMultipleUrls } from '@/lib/scraper'
import { GenerateRequest } from '@/types'

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

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

    const prompt = `あなたはプロのブログライターです。以下の情報をもとに、オリジナルのブログ記事を日本語で作成してください。

## あなたのブログコンテンツ（文体・スタイルの参考）
タイトル: ${blogContent.title}
URL: ${blogContent.url}

内容:
${blogContent.content}
${referenceSection}${ngWordsText}${closingSection}${customSection}

## 記事作成のルール
1. 上記のブログコンテンツから文体、トーン、語り口を学習し、同じスタイルで新しい記事を書いてください
2. コンテンツの内容を参考にしながら、独自の視点を加えた新しい記事を作成してください
3. 読者が最後まで読みたくなるような構成にしてください
4. 見出し（#, ##）を使って読みやすく整理してください
5. NGワードは絶対に使用しないでください
6. 定型文がある場合は、記事の最後に必ず追加してください

それでは、上記のスタイルに合わせたブログ記事を作成してください:`

    const response = await client.messages.create({
      model: 'claude-opus-4-5',
      max_tokens: 3000,
      messages: [{ role: 'user', content: prompt }]
    })

    const article = response.content
      .filter(block => block.type === 'text')
      .map(block => (block as { type: 'text'; text: string }).text)
      .join('\n')

    return NextResponse.json({ success: true, article })
  } catch (error) {
    console.error('Generation error:', error)
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : '記事生成中にエラーが発生しました' },
      { status: 500 }
    )
  }
}
