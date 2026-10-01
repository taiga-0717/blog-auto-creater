import { Settings } from '@/types'

const SETTINGS_KEY = 'blog-generator-settings'

export const defaultSettings: Settings = {
  blogIndexUrl: '',
  referenceLinks: [],
  ngWords: [],
  closingText: '',
  fixedImages: [],
  wordpress: {
    siteUrl: '',
    username: '',
    appPassword: ''
  }
}

export function loadSettings(): Settings {
  if (typeof window === 'undefined') return defaultSettings
  try {
    const stored = localStorage.getItem(SETTINGS_KEY)
    if (!stored) return defaultSettings
    const parsed = JSON.parse(stored)
    return {
      ...defaultSettings,
      ...parsed,
      wordpress: { ...defaultSettings.wordpress, ...parsed.wordpress }
    }
  } catch {
    return defaultSettings
  }
}

// 保存に失敗した場合（画像が大きすぎて容量オーバーなど）は false を返す
export function saveSettings(settings: Settings): boolean {
  if (typeof window === 'undefined') return false
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
    return true
  } catch {
    return false
  }
}
