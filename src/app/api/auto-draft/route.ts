import { NextRequest, NextResponse } from 'next/server'
import { runAutoDraft } from '@/lib/autoPost'
import { whoAmI } from '@/lib/wordpress'

// アプリの「自動投稿」タブから手動で下書きを作る / 接続テストする
export const dynamic = 'force-dynamic'
export const maxDuration = 300

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()
    const { password, action, memo, theme } = body as {
      password?: string
      action?: 'test' | 'create'
      memo?: string
      theme?: string
    }

    const adminPassword = process.env.ADMIN_PASSWORD
    if (!adminPassword) {
      return NextResponse.json({ success: false, error: 'ADMIN_PASSWORD が設定されていません' }, { status: 500 })
    }
    if (password !== adminPassword) {
      return NextResponse.json({ success: false, error: 'パスワードが違います' }, { status: 401 })
    }

    if (action === 'test') {
      const me = await whoAmI()
      return NextResponse.json({ success: true, message: `WordPressに「${me.name}」として接続できました` })
    }

    const result = await runAutoDraft({ memo, themeOverride: theme })
    return NextResponse.json({ success: true, ...result })
  } catch (error) {
    console.error('[auto-draft] failed:', error)
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : '下書きの作成に失敗しました' },
      { status: 500 }
    )
  }
}
