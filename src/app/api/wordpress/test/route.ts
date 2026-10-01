import { NextRequest, NextResponse } from 'next/server'
import { WordPressSettings } from '@/types'
import { validateWordPressSettings, wpErrorMessage, wpFetch } from '@/lib/wordpress'

// 国内レンタルサーバーは海外IPからのREST APIアクセスを制限していることが多いため、東京リージョンで実行する
export const preferredRegion = 'hnd1'

export async function POST(req: NextRequest) {
  try {
    const { wordpress }: { wordpress: WordPressSettings } = await req.json()
    const invalid = validateWordPressSettings(wordpress)
    if (invalid) return NextResponse.json({ success: false, error: invalid }, { status: 400 })

    const res = await wpFetch(wordpress, '/users/me?context=edit')
    if (!res.ok) return NextResponse.json({ success: false, error: await wpErrorMessage(res) }, { status: 400 })
    const user = await res.json()
    return NextResponse.json({ success: true, name: user.name })
  } catch (error) {
    console.error('WordPress test error:', error)
    return NextResponse.json(
      { success: false, error: error instanceof Error ? `WordPressに接続できませんでした（${error.message}）` : 'WordPressに接続できませんでした' },
      { status: 500 }
    )
  }
}
