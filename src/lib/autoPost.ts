import Anthropic from '@anthropic-ai/sdk'
import { autoPostConfig } from '@/config/autoPost'
import { createDraft, getRecentPosts, CreatedDraft, WpPostSummary } from '@/lib/wordpress'

// 自動生成した下書きの目印（本文末尾のHTMLコメント。表示はされません）
export const AUTO_MARKER = '<!-- blog-auto-creater -->'

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

export interface RunOptions {
  /** 校舎のできごと・お知らせなどのメモ。あればこれを記事の主題にする */
  memo?: string
  /** テーマを直接指定したいとき */
  themeOverride?: string
  /** 今日すでに自動下書きがあれば作らない（毎日の定期実行用） */
  skipIfAlreadyToday?: boolean
}

export type RunResult =
  | { status: 'skipped'; reason: string }
  | { status: 'created'; title: string; theme: string; draft: CreatedDraft }

// ---------- 日付（日本時間） ----------

function jstParts(d = new Date()) {
  const j = new Date(d.getTime() + 9 * 60 * 60 * 1000)
  return {
    year: j.getUTCFullYear(),
    month: j.getUTCMonth() + 1,
    day: j.getUTCDate(),
    weekday: j.getUTCDay(),
  }
}

/** 日本時間の今日0時を、WordPressの after= に渡せるUTCのISO文字列で返す */
function jstMidnightIso(): string {
  const { year, month, day } = jstParts()
  return new Date(Date.UTC(year, month - 1, day, -9, 0, 0)).toISOString()
}

function seasonHint(month: number): string {
  const hints: Record<number, string> = {
    1: '冬期講習明け・私立入試直前・学年末に向けた時期',
    2: '埼玉県公立入試直前・学年末テストの時期',
    3: '公立入試後・春期講習・新学年準備の時期',
    4: '新学年スタート・学習習慣づくりの時期',
    5: '中間テスト前・部活との両立が課題になる時期',
    6: '中間テスト明け〜期末テスト前の時期',
    7: '期末テスト明け・夏期講習・夏休みの計画の時期',
    8: '夏休み後半・宿題の仕上げ・受験生の天王山の時期',
    9: '2学期スタート・北辰テスト・中間テスト/前期期末テストの時期',
    10: '中間テスト・後期スタート・志望校選びが本格化する時期',
    11: '期末テスト・内申が固まる大事な時期',
    12: '冬期講習・受験直前期・学期末の時期',
  }
  return hints[month] ?? ''
}

const WEEKDAY_JA = ['日', '月', '火', '水', '木', '金', '土']

// ---------- 記事の構造化出力 ----------

type Block =
  | { type: 'h2' | 'h3' | 'p'; text: string }
  | { type: 'ul' | 'ol'; items: string[] }

interface ArticleOutput {
  title: string
  slug: string
  meta_description: string
  tags: string[]
  blocks: Block[]
}

const articleTool: Anthropic.Tool = {
  name: 'save_article',
  description: '完成したブログ記事をWordPressの下書きとして保存する',
  input_schema: {
    type: 'object',
    properties: {
      title: {
        type: 'string',
        description: 'SEOを意識した記事タイトル（28〜35文字程度。主要キーワードを前半に）',
      },
      slug: {
        type: 'string',
        description: 'URL用のスラッグ。半角英小文字・数字・ハイフンのみ（例: kawagoe-teiki-test-taisaku）',
      },
      meta_description: {
        type: 'string',
        description: '検索結果に表示される説明文（80〜120文字。キーワードと記事の要点を含める）',
      },
      tags: {
        type: 'array',
        items: { type: 'string' },
        description: 'WordPressのタグ（3〜5個。短い日本語の語句）',
      },
      blocks: {
        type: 'array',
        description: '本文。見出し(h2/h3)・段落(p)・箇条書き(ul/ol)の配列。タイトル(h1)は含めない。強調したい語句は **太字** で囲む',
        items: {
          type: 'object',
          properties: {
            type: { type: 'string', enum: ['h2', 'h3', 'p', 'ul', 'ol'] },
            text: { type: 'string', description: 'h2 / h3 / p のときの文章' },
            items: { type: 'array', items: { type: 'string' }, description: 'ul / ol のときの各項目' },
          },
          required: ['type'],
        },
      },
    },
    required: ['title', 'slug', 'meta_description', 'tags', 'blocks'],
  },
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

function inline(s: string): string {
  return escapeHtml(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
}

function blocksToHtml(blocks: Block[]): string {
  return blocks
    .map(b => {
      if (b.type === 'ul' || b.type === 'ol') {
        const items = (b.items || []).filter(Boolean)
        if (!items.length) return ''
        return `<${b.type}>\n${items.map(i => `<li>${inline(i)}</li>`).join('\n')}\n</${b.type}>`
      }
      const text = (b as { text?: string }).text?.trim()
      if (!text) return ''
      if (b.type === 'p') {
        return text
          .split(/\n{2,}/)
          .map(para => `<p>${inline(para).replace(/\n/g, '<br>')}</p>`)
          .join('\n')
      }
      return `<${b.type}>${inline(text)}</${b.type}>`
    })
    .filter(Boolean)
    .join('\n\n')
}

function cleanSlug(slug: string): string {
  const s = slug
    .toLowerCase()
    .replace(/[^a-z0-9-]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 60)
  return s || `blog-${Date.now()}`
}

// ---------- プロンプト ----------

function buildPrompt(opts: {
  theme: string
  memo?: string
  styleSamples: WpPostSummary[]
  recentTitles: string[]
}): string {
  const c = autoPostConfig
  const { year, month, day, weekday } = jstParts()

  const style = opts.styleSamples.length
    ? opts.styleSamples
        .map((p, i) => `【過去記事${i + 1}】${p.title}\n${p.contentText.slice(0, 1500)}`)
        .join('\n\n---\n\n')
    : '（取得できませんでした。個別指導塾の校舎ブログらしい、親しみやすく丁寧な「です・ます」調で書いてください）'

  const memoSection = opts.memo?.trim()
    ? `\n## 今日の校舎メモ（この内容を記事の中心にする）\n${opts.memo.trim()}\n\nメモに書かれている事実だけを使い、書かれていない具体的な出来事・人数・成績・日程は作らないでください。メモの内容を膨らませるときは、その出来事から保護者・生徒に役立つ学びやアドバイスにつなげてください。\n`
    : ''

  const ng = c.ngWords.length ? `\n## 使用禁止ワード\n${c.ngWords.map(w => `- ${w}`).join('\n')}\n` : ''

  const closing = c.closingText.trim()
    ? `\n## 記事末尾の定型文\n本文の最後の段落として、次の文章をそのまま入れてください:\n${c.closingText.trim()}\n`
    : ''

  return `あなたは「${c.schoolName} ${c.campusName}」（${c.area}の個別指導塾）の校舎ブログを担当する講師です。
今日のブログ記事を1本書き、save_article ツールで保存してください。

## 今日の日付
${year}年${month}月${day}日（${WEEKDAY_JA[weekday]}）— ${seasonHint(month)}

## 今日のテーマ
${opts.theme}
${memoSection}
## 読者
川越市（新河岸・南古谷周辺）に住む小中高生の保護者と生徒。塾選びや成績アップに悩んでいる人。

## SEO（検索対策）
- 次のキーワードから記事に合うものを1〜2個選び、タイトル・最初の段落・h2見出しのどれかに自然に入れる: ${c.seoKeywords.join(' / ')}
- 「川越」「新河岸」などの地域名を本文中に自然に2〜3回入れる（詰め込みすぎない）
- 見出しは h2 を3〜5個、必要に応じて h3。見出しだけ読んでも内容がわかるように
- 最初の段落で「この記事で何がわかるか」を簡潔に示す
- 本文は${c.targetLength}。読者の悩みに具体的に答える、役立つ内容にする
- 最後は${c.campusName}への無料体験・学習相談につながる自然な締めにする（押し売りしない）

## 過去の記事（文体・トーンを合わせる参考。内容はコピーしない）
${style}

## 最近の記事タイトル（これらとテーマ・切り口が重ならないようにする）
${opts.recentTitles.length ? opts.recentTitles.map(t => `- ${t}`).join('\n') : '（なし）'}
${ng}${closing}
## 守ること
- 校舎の実績・合格者数・生徒の点数・料金・キャンペーン・日程など、確認できない具体的な事実は作らない
- 入試制度や日程など、正確さに自信がない情報を書く場合は、その文の末尾に【要確認】と付ける（公開前に講師が確認します）
- 他塾の悪口や、「必ず」「絶対に上がる」などの誇大表現は使わない
- 生徒の実名は出さない`
}

// ---------- 実行 ----------

export async function runAutoDraft(opts: RunOptions = {}): Promise<RunResult> {
  if (!process.env.ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY が設定されていません')

  // 1. 今日すでに自動下書きがあるか（定期実行時のみ確認）
  if (opts.skipIfAlreadyToday) {
    const todays = await getRecentPosts(['draft', 'pending', 'future', 'publish'], 20, `&after=${encodeURIComponent(jstMidnightIso())}`)
    const already = todays.find(p => p.contentRaw?.includes(AUTO_MARKER))
    if (already) {
      return { status: 'skipped', reason: `今日はすでに自動下書きがあります（${already.title}）` }
    }
  }

  // 2. 文体の参考と、重複回避用のタイトル一覧
  let styleSamples: WpPostSummary[] = []
  let recentTitles: string[] = []
  try {
    const recent = await getRecentPosts(['publish', 'draft', 'future'], 40)
    recentTitles = recent.map(p => p.title).filter(Boolean)
    styleSamples = recent.filter(p => p.status === 'publish' && p.contentText.length > 300).slice(0, 3)
  } catch (e) {
    console.warn('過去記事の取得に失敗（続行します）:', e)
  }

  // 3. テーマ決定
  const { weekday } = jstParts()
  const theme = opts.memo?.trim()
    ? `${autoPostConfig.campusName}の最近の様子・お知らせ（下の「今日の校舎メモ」をもとに）`
    : opts.themeOverride?.trim() || autoPostConfig.weekdayThemes[weekday]

  // 4. 記事生成
  const response = await client.messages.create({
    model: process.env.ANTHROPIC_MODEL || 'claude-opus-4-5',
    max_tokens: 8000,
    tools: [articleTool],
    tool_choice: { type: 'tool', name: 'save_article' },
    messages: [{ role: 'user', content: buildPrompt({ theme, memo: opts.memo, styleSamples, recentTitles }) }],
  })

  const toolUse = response.content.find(b => b.type === 'tool_use') as Anthropic.ToolUseBlock | undefined
  if (!toolUse) throw new Error('記事の生成結果を受け取れませんでした')
  const article = toolUse.input as ArticleOutput
  if (!article.title || !Array.isArray(article.blocks) || article.blocks.length === 0) {
    throw new Error('生成された記事の形式が正しくありません')
  }

  // 5. WordPressに下書き保存
  const content = `${blocksToHtml(article.blocks)}\n\n${AUTO_MARKER}`
  const draft = await createDraft({
    title: article.title,
    content,
    excerpt: article.meta_description,
    slug: cleanSlug(article.slug),
    tagNames: article.tags || [],
  })

  return { status: 'created', title: article.title, theme, draft }
}
