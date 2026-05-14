import { Settings } from '@/types'

const SETTINGS_KEY = 'blog-generator-settings'

export const defaultSettings: Settings = {
  blogIndexUrl: '',
  referenceLinks: [],
  ngWords: [],
  closingText: ''
}

export function loadSettings(): Settings {
  if (typeof window === 'undefined') return defaultSettings
  try {
    const stored = localStorage.getItem(SETTINGS_KEY)
    if (!stored) return defaultSettings
    return { ...defaultSettings, ...JSON.parse(stored) }
  } catch {
    return defaultSettings
  }
}

export function saveSettings(settings: Settings): void {
  if (typeof window === 'undefined') return
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
}
