import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'ブログ記事ジェネレーター',
  description: 'あなたのブログスタイルで新しい記事を自動生成',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  )
}
