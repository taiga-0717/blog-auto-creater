// WordPress REST API クライアント（アプリケーションパスワード認証）
//
// 必要な環境変数:
//   WP_BASE_URL          例: https://meiseikobetsu.jp
//   WP_USERNAME          WordPressのユーザー名
//   WP_APP_PASSWORD      ユーザー → プロフィールで発行したアプリケーションパスワード
//   WP_CATEGORY_IDS      （任意）下書きに付けるカテゴリーID。カンマ区切り 例: 12,34

export interface WpPostSummary {
  id: number
  date: string
  status: string
  title: string
  link: string
  contentText: string
  contentRaw?: string
}

export interface CreateDraftInput {
  title: string
  content: string
  excerpt: string
  slug: string
  tagNames: string[]
}

export interface CreatedDraft {
  id: number
  editUrl: string
  previewUrl: string
}

function getEnv() {
  const base = process.env.WP_BASE_URL?.replace(/\/+$/, '')
  const user = process.env.WP_USERNAME
  const pass = process.env.WP_APP_PASSWORD?.replace(/\s+/g, '')
  if (!base || !user || !pass) {
    throw new Error('WordPressの環境変数（WP_BASE_URL / WP_USERNAME / WP_APP_PASSWORD）が設定されていません')
  }
  return { base, auth: 'Basic ' + Buffer.from(`${user}:${pass}`).toString('base64') }
}

async function wp<T>(path: string, init: RequestInit = {}): Promise<T> {
  const { base, auth } = getEnv()
  const res = await fetch(`${base}/wp-json${path}`, {
    ...init,
    headers: {
      Authorization: auth,
      'Content-Type': 'application/json',
      Accept: 'application/json',
      'User-Agent': 'Mozilla/5.0 (compatible; MeiseiBlogAutoDraft/1.0)',
      ...(init.headers || {}),
    },
    cache: 'no-store',
  })
  const text = await res.text()
  if (!res.ok) {
    let message = text.slice(0, 300)
    try {
      const j = JSON.parse(text)
      if (j?.message) message = `${j.code ?? ''} ${j.message}`.trim()
    } catch {}
    throw new Error(`WordPress API エラー (${res.status}) ${path}: ${message}`)
  }
  try {
    return JSON.parse(text) as T
  } catch {
    throw new Error(`WordPress API の応答がJSONではありません (${path})。セキュリティプラグイン等でREST APIがブロックされている可能性があります`)
  }
}

function stripHtml(html: string): string {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&#8217;|&#8216;/g, "'")
    .replace(/&#8220;|&#8221;/g, '"')
    .replace(/&#\d+;/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function decodeTitle(s: string): string {
  return stripHtml(s)
}

interface RawPost {
  id: number
  date: string
  status: string
  link: string
  title: { rendered: string; raw?: string }
  content: { rendered: string; raw?: string }
}

/** 接続テスト：認証ユーザーの名前を返す */
export async function whoAmI(): Promise<{ id: number; name: string }> {
  const me = await wp<{ id: number; name: string }>('/wp/v2/users/me?context=edit')
  return { id: me.id, name: me.name }
}

/** 最近の投稿（公開済み・下書き・予約など）を取得 */
export async function getRecentPosts(
  statuses: string[] = ['publish'],
  perPage = 20,
  extraQuery = ''
): Promise<WpPostSummary[]> {
  const q = `/wp/v2/posts?context=edit&per_page=${perPage}&orderby=date&order=desc&status=${statuses.join(',')}${extraQuery}`
  const posts = await wp<RawPost[]>(q)
  return posts.map(p => ({
    id: p.id,
    date: p.date,
    status: p.status,
    title: decodeTitle(p.title.raw ?? p.title.rendered),
    link: p.link,
    contentText: stripHtml(p.content.rendered),
    contentRaw: p.content.raw,
  }))
}

/** タグ名からIDを取得（なければ作成） */
async function resolveTagIds(names: string[]): Promise<number[]> {
  const ids: number[] = []
  for (const name of names.map(n => n.trim()).filter(Boolean).slice(0, 8)) {
    try {
      const found = await wp<{ id: number; name: string }[]>(
        `/wp/v2/tags?search=${encodeURIComponent(name)}&per_page=20`
      )
      const exact = found.find(t => decodeTitle(t.name) === name)
      if (exact) {
        ids.push(exact.id)
        continue
      }
      const created = await wp<{ id: number }>('/wp/v2/tags', {
        method: 'POST',
        body: JSON.stringify({ name }),
      })
      ids.push(created.id)
    } catch (e) {
      // タグが作れなくても下書き作成は続ける
      console.warn(`タグ「${name}」の設定に失敗:`, e)
    }
  }
  return ids
}

/** 下書きとして投稿を作成 */
export async function createDraft(input: CreateDraftInput): Promise<CreatedDraft> {
  const { base } = getEnv()
  const categories = (process.env.WP_CATEGORY_IDS || '')
    .split(',')
    .map(s => parseInt(s.trim(), 10))
    .filter(n => !Number.isNaN(n))

  const tags = await resolveTagIds(input.tagNames)

  const body: Record<string, unknown> = {
    status: 'draft',
    title: input.title,
    content: input.content,
    excerpt: input.excerpt,
    slug: input.slug,
  }
  if (categories.length) body.categories = categories
  if (tags.length) body.tags = tags

  const post = await wp<{ id: number; link: string }>('/wp/v2/posts', {
    method: 'POST',
    body: JSON.stringify(body),
  })

  return {
    id: post.id,
    editUrl: `${base}/wp-admin/post.php?post=${post.id}&action=edit`,
    previewUrl: `${base}/?p=${post.id}&preview=true`,
  }
}
