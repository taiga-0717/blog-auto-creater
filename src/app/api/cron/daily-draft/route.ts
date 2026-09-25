import { NextRequest, NextResponse } from 'next/server'
import { runAutoDraft } from '@/lib/autoPost'

// Vercel Cron から毎日呼ばれる（vercel.json の crons を参照）
export const dynamic = 'force-dynamic'
export const maxDuration = 300

export async function GET(req: NextRequest) {
  const secret = process.env.CRON_SECRET
  if (!secret || req.headers.get('authorization') !== `Bearer ${secret}`) {
    return NextResponse.json({ success: false, error: 'unauthorized' }, { status: 401 })
  }

  try {
    const result = await runAutoDraft({ skipIfAlreadyToday: true })
    console.log('[daily-draft]', JSON.stringify(result))
    return NextResponse.json({ success: true, ...result })
  } catch (error) {
    console.error('[daily-draft] failed:', error)
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : '自動下書きの作成に失敗しました' },
      { status: 500 }
    )
  }
}
