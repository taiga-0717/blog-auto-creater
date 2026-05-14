export interface Settings {
  blogIndexUrl: string
  referenceLinks: string[]
  ngWords: string[]
  closingText: string
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
