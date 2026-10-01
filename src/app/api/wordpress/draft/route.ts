import { NextRequest, NextResponse } from 'next/server'
import { WordPressDraftRequest } from '@/types'
import { imageHtml } from '@/lib/markdown'
import {
  editUrl,
  previewUrl,
  uploadDataUrlImage,
  validateWordPressSettings,
  wpErrorMessage,
  wpFetch
} from '@/lib/wordpress'

export async function POST(req: NextRequest) {
  try {
    const { wordpress, title, content, images }: WordPressDraftRequest = await req.json()
    const invalid = validateWordPressSettings(wordpress)
    if (invalid) return NextResponse.json({ success: false, error: invalid }, { status: 400 })
    if (!content?.trim()) {
      return NextResponse.json({ success: false, error: '記事の本文が空です' }, { status: 400 })
    }

    // アップロード画像（data URL）はメディアライブラリへ登録してから本文に差し込む
    const uploadedImages: Record<string, string> = {}
    const resolved: { position: string; html: string }[] = []
    for (const image of images || []) {
      let src = image.src
      if (src.startsWith('data:')) {
        src = await uploadDataUrlImage(wordpress, src, image.alt, `blog-fixed-image-${image.id}`)
        uploadedImages[image.id] = src
      }
      resolved.push({ position: image.position, html: imageHtml(src, image.alt) })
    }

    const top = resolved.filter(i => i.position === 'top').map(i => i.html)
    const bottom = resolved.filter(i => i.position === 'bottom').map(i => i.html)
    const fullContent = [...top, content, ...bottom].join('\n')

    const res = await wpFetch(wordpress, '/posts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: title || '無題の下書き',
        content: fullContent,
        status: 'draft'
      })
    })
    if (!res.ok) {
      return NextResponse.json({ success: false, error: await wpErrorMessage(res), uploadedImages }, { status: 400 })
    }
    const post = await res.json()

    return NextResponse.json({
      success: true,
      postId: post.id,
      editUrl: editUrl(wordpress, post.id),
      previewUrl: previewUrl(wordpress, post.id),
      uploadedImages
    })
  } catch (error) {
    console.error('WordPress draft error:', error)
    return NextResponse.json(
      { success: false, error: error instanceof Error ? error.message : 'WordPressへの送信中にエラーが発生しました' },
      { status: 500 }
    )
  }
}
