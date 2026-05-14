import * as cheerio from 'cheerio'
import { ScrapedContent } from '@/types'

export async function scrapeUrl(url: string): Promise<ScrapedContent> {
  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; BlogGeneratorBot/1.0)',
      },
      next: { revalidate: 3600 }
    })

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`)
    }

    const html = await response.text()
    const $ = cheerio.load(html)

    // タイトル取得
    const title = $('title').text() || $('h1').first().text() || url

    // 不要な要素を削除
    $('script, style, nav, footer, header, aside, .sidebar, .menu, .advertisement, .ads, [class*="ad-"], [id*="ad-"]').remove()

    // メインコンテンツを抽出（優先順位付き）
    let content = ''
    const contentSelectors = [
      'article',
      'main',
      '.post-content',
      '.entry-content',
      '.article-content',
      '.blog-content',
      '#content',
      '.content'
    ]

    for (const selector of contentSelectors) {
      const el = $(selector)
      if (el.length && el.text().trim().length > 100) {
        content = el.text().trim()
        break
      }
    }

    // フォールバック: bodyから抽出
    if (!content) {
      content = $('body').text().trim()
    }

    // 余分な空白を整理
    content = content.replace(/\s+/g, ' ').trim()

    // 長すぎる場合は最初の5000文字に制限
    if (content.length > 5000) {
      content = content.substring(0, 5000) + '...'
    }

    return { url, title: title.trim(), content }
  } catch (error) {
    console.error(`Failed to scrape ${url}:`, error)
    return {
      url,
      title: url,
      content: `（このURLのコンテンツを取得できませんでした: ${error instanceof Error ? error.message : 'Unknown error'}）`
    }
  }
}

export async function scrapeMultipleUrls(urls: string[]): Promise<ScrapedContent[]> {
  const results = await Promise.allSettled(urls.map(url => scrapeUrl(url)))
  return results.map((result, i) => {
    if (result.status === 'fulfilled') return result.value
    return { url: urls[i], title: urls[i], content: '（取得失敗）' }
  })
}
