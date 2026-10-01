import { WordPressSettings } from '@/types'

export function normalizeSiteUrl(url: string): string {
  return url.trim().replace(/\/+$/, '').replace(/\/wp-admin$/, '')
}

export function validateWordPressSettings(wp: WordPressSettings | undefined): string | null {
  if (!wp || !wp.siteUrl?.trim() || !wp.username?.trim() || !wp.appPassword?.trim()) {
    return 'WordPressの接続情報（サイトURL・ユーザー名・アプリケーションパスワード）を設定タブで入力してください'
  }
  if (!/^https?:\/\//i.test(wp.siteUrl.trim())) {
    return 'WordPressのサイトURLは https:// から始まる形式で入力してください'
  }
  return null
}

function authHeader(wp: WordPressSettings): string {
  // アプリケーションパスワードは空白入りで表示されるが、空白を除いても有効
  const password = wp.appPassword.replace(/\s+/g, '')
  return 'Basic ' + Buffer.from(`${wp.username.trim()}:${password}`).toString('base64')
}

// /wp-json/wp/v2/... を呼び出す。パーマリンク設定が「基本」のサイト向けに ?rest_route= へフォールバックする
export async function wpFetch(wp: WordPressSettings, path: string, init: RequestInit = {}): Promise<Response> {
  const site = normalizeSiteUrl(wp.siteUrl)
  const headers = { ...(init.headers as Record<string, string>), Authorization: authHeader(wp) }
  const res = await fetch(`${site}/wp-json/wp/v2${path}`, { ...init, headers, cache: 'no-store' })
  if (res.status !== 404) return res
  const [route, query] = path.split('?')
  const fallback = `${site}/?rest_route=/wp/v2${route}${query ? `&${query}` : ''}`
  return fetch(fallback, { ...init, headers, cache: 'no-store' })
}

export async function wpErrorMessage(res: Response): Promise<string> {
  let detail = ''
  try {
    const data = await res.json()
    detail = data?.message ? `（${String(data.message).replace(/<[^>]+>/g, '')}）` : ''
  } catch {
    // JSON以外のレスポンス
  }
  if (res.status === 401) return `WordPressの認証に失敗しました。ユーザー名とアプリケーションパスワードを確認してください${detail}`
  if (res.status === 403) return `このユーザーには投稿・アップロードの権限がありません${detail}`
  if (res.status === 404) return `WordPressのREST APIが見つかりません。サイトURLを確認してください${detail}`
  return `WordPressへのリクエストが失敗しました（HTTP ${res.status}）${detail}`
}

export function editUrl(wp: WordPressSettings, postId: number): string {
  return `${normalizeSiteUrl(wp.siteUrl)}/wp-admin/post.php?post=${postId}&action=edit`
}

export function previewUrl(wp: WordPressSettings, postId: number): string {
  return `${normalizeSiteUrl(wp.siteUrl)}/?p=${postId}&preview=true`
}

const EXTENSIONS: Record<string, string> = {
  'image/jpeg': 'jpg',
  'image/png': 'png',
  'image/gif': 'gif',
  'image/webp': 'webp'
}

// data URL の画像をメディアライブラリにアップロードし、公開URLを返す
export async function uploadDataUrlImage(wp: WordPressSettings, dataUrl: string, alt: string, name: string): Promise<string> {
  const m = dataUrl.match(/^data:(image\/[a-z+]+);base64,(.+)$/i)
  if (!m) throw new Error('画像データの形式が正しくありません')
  const mime = m[1].toLowerCase()
  const buffer = Buffer.from(m[2], 'base64')
  const filename = `${name}.${EXTENSIONS[mime] || 'jpg'}`

  const res = await wpFetch(wp, '/media', {
    method: 'POST',
    headers: {
      'Content-Type': mime,
      'Content-Disposition': `attachment; filename="${filename}"`
    },
    body: buffer
  })
  if (!res.ok) throw new Error(await wpErrorMessage(res))
  const media = await res.json()

  if (alt) {
    await wpFetch(wp, `/media/${media.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ alt_text: alt })
    }).catch(() => undefined)
  }
  return media.source_url as string
}
