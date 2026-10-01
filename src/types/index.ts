export type ImagePosition = 'top' | 'bottom'

export interface FixedImage {
  id: string
  // 外部URL、またはアップロードした画像のdata URL
  src: string
  alt: string
  position: ImagePosition
  // WordPressへアップロード済みの場合のURL（再アップロードを防ぐため）
  wpMediaUrl?: string
  wpMediaSite?: string
}

export interface WordPressSettings {
  siteUrl: string
  username: string
  appPassword: string
}

export interface Settings {
  blogIndexUrl: string
  referenceLinks: string[]
  ngWords: string[]
  closingText: string
  fixedImages: FixedImage[]
  wordpress: WordPressSettings
}

export interface GenerateRequest {
  blogIndexUrl: string
  referenceLinks: string[]
  ngWords: string[]
  closingText: string
  customInstruction?: string
}

export interface GenerateResponse {
  success: boolean
  article?: string
  error?: string
}

export interface ScrapedContent {
  url: string
  title: string
  content: string
}

export interface WordPressImagePayload {
  id: string
  src: string
  alt: string
  position: ImagePosition
}

export interface WordPressDraftRequest {
  wordpress: WordPressSettings
  title: string
  // 本文のHTML（固定画像を除く）
  content: string
  images: WordPressImagePayload[]
}

export interface WordPressDraftResponse {
  success: boolean
  postId?: number
  editUrl?: string
  previewUrl?: string
  // アップロードした画像のid → WordPress上のURL
  uploadedImages?: Record<string, string>
  error?: string
}
