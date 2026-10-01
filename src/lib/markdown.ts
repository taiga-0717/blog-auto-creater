import { FixedImage } from '@/types'

export function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function safeUrl(url: string): string {
  return /^(https?:|mailto:|\/|#)/i.test(url) ? url : '#'
}

function renderInline(text: string): string {
  return escapeHtml(text)
    .replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (_, alt, url) => `<img src="${safeUrl(url)}" alt="${alt}" />`)
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, label, url) => `<a href="${safeUrl(url)}">${label}</a>`)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*\s][^*]*?)\*/g, '$1<em>$2</em>')
    .replace(/(^|[\s(（])(https?:\/\/[^\s<)）]+)/g, '$1<a href="$2">$2</a>')
}

// 生成された記事（Markdown）をHTMLに変換する
export function markdownToHtml(markdown: string): string {
  const lines = markdown.replace(/\r\n/g, '\n').split('\n')
  const out: string[] = []
  let paragraph: string[] = []
  let list: { tag: 'ul' | 'ol'; items: string[] } | null = null
  let quote: string[] = []

  const flushParagraph = () => {
    if (paragraph.length) out.push(`<p>${paragraph.map(renderInline).join('<br />')}</p>`)
    paragraph = []
  }
  const flushList = () => {
    if (list) out.push(`<${list.tag}>${list.items.map(i => `<li>${renderInline(i)}</li>`).join('')}</${list.tag}>`)
    list = null
  }
  const flushQuote = () => {
    if (quote.length) out.push(`<blockquote><p>${quote.map(renderInline).join('<br />')}</p></blockquote>`)
    quote = []
  }
  const flushAll = () => {
    flushParagraph()
    flushList()
    flushQuote()
  }

  for (const raw of lines) {
    const line = raw.trimEnd()
    let m: RegExpMatchArray | null

    if (!line.trim()) {
      flushAll()
    } else if ((m = line.match(/^(#{1,6})\s+(.+)$/))) {
      flushAll()
      const level = m[1].length
      out.push(`<h${level}>${renderInline(m[2])}</h${level}>`)
    } else if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      flushAll()
      out.push('<hr />')
    } else if ((m = line.match(/^\s*[-*+]\s+(.+)$/))) {
      flushParagraph()
      flushQuote()
      if (!list || list.tag !== 'ul') {
        flushList()
        list = { tag: 'ul', items: [] }
      }
      list.items.push(m[1])
    } else if ((m = line.match(/^\s*\d+[.)]\s+(.+)$/))) {
      flushParagraph()
      flushQuote()
      if (!list || list.tag !== 'ol') {
        flushList()
        list = { tag: 'ol', items: [] }
      }
      list.items.push(m[1])
    } else if ((m = line.match(/^>\s?(.*)$/))) {
      flushParagraph()
      flushList()
      quote.push(m[1])
    } else {
      flushList()
      flushQuote()
      paragraph.push(line)
    }
  }
  flushAll()
  return out.join('\n')
}

// 記事の先頭にある「# タイトル」を取り出し、本文と分ける
export function splitTitle(markdown: string): { title: string; body: string } {
  const lines = markdown.replace(/\r\n/g, '\n').split('\n')
  const index = lines.findIndex(l => l.trim() !== '')
  if (index >= 0) {
    const m = lines[index].match(/^#\s+(.+)$/)
    if (m) {
      return { title: m[1].replace(/\*\*/g, '').trim(), body: lines.slice(index + 1).join('\n').trim() }
    }
  }
  return { title: '', body: markdown.trim() }
}

export function imageHtml(src: string, alt: string): string {
  return `<figure class="wp-block-image size-large"><img src="${escapeHtml(src)}" alt="${escapeHtml(alt)}" /></figure>`
}

// プレビュー用：固定画像をタイトル直後・末尾に差し込んだHTML
export function buildArticleHtml(markdown: string, images: FixedImage[]): string {
  const { title, body } = splitTitle(markdown)
  const top = images.filter(i => i.position === 'top').map(i => imageHtml(i.src, i.alt))
  const bottom = images.filter(i => i.position === 'bottom').map(i => imageHtml(i.src, i.alt))
  const heading = title ? [`<h1>${renderInline(title)}</h1>`] : []
  return [...heading, ...top, markdownToHtml(body), ...bottom].join('\n')
}

// コピー用：URL指定の固定画像をMarkdownとして差し込む
// （アップロード画像はWordPressへ送信済みでなければデータが巨大なため含めない）
export function buildArticleMarkdown(markdown: string, images: FixedImage[]): string {
  const { title, body } = splitTitle(markdown)
  const toMd = (i: FixedImage) => {
    const url = i.wpMediaUrl || i.src
    return url.startsWith('data:') ? null : `![${i.alt}](${url})`
  }
  const top = images.filter(i => i.position === 'top').map(toMd).filter(Boolean)
  const bottom = images.filter(i => i.position === 'bottom').map(toMd).filter(Boolean)
  const heading = title ? [`# ${title}`] : []
  return [...heading, ...top, body, ...bottom].join('\n\n')
}
