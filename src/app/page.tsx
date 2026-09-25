'use client'

import { useState, useEffect, useCallback } from 'react'
import { Settings } from '@/types'
import { loadSettings, saveSettings } from '@/lib/settings'
import styles from './page.module.css'

function parseMarkdown(text: string): string {
  return text
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*<\/li>)/, '<ul>$1</ul>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(?!<[h|u|b|l])(.+)$/gm, (m) => m.startsWith('<') ? m : `<p>${m}</p>`)
    .replace(/<p><\/p>/g, '')
}

export default function Home() {
  const [settings, setSettings] = useState<Settings>({
    blogIndexUrl: '',
    referenceLinks: [],
    ngWords: [],
    closingText: ''
  })
  const [newRefLink, setNewRefLink] = useState('')
  const [newNgWord, setNewNgWord] = useState('')
  const [customInstruction, setCustomInstruction] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [article, setArticle] = useState('')
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState<'generate' | 'auto' | 'settings'>('generate')
  const [adminPassword, setAdminPassword] = useState('')
  const [memo, setMemo] = useState('')
  const [autoTheme, setAutoTheme] = useState('')
  const [autoBusy, setAutoBusy] = useState<'' | 'test' | 'create'>('')
  const [autoMessage, setAutoMessage] = useState('')
  const [autoError, setAutoError] = useState('')
  const [autoEditUrl, setAutoEditUrl] = useState('')
  const [settingsSaved, setSettingsSaved] = useState(false)
  const [copyDone, setCopyDone] = useState(false)

  useEffect(() => {
    setSettings(loadSettings())
    try {
      setAdminPassword(localStorage.getItem('blog-generator-admin-password') || '')
    } catch {}
  }, [])

  const handleAutoDraft = async (action: 'test' | 'create') => {
    if (!adminPassword) {
      setAutoError('パスワードを入力してください')
      return
    }
    try {
      localStorage.setItem('blog-generator-admin-password', adminPassword)
    } catch {}
    setAutoBusy(action)
    setAutoError('')
    setAutoMessage('')
    setAutoEditUrl('')
    try {
      const response = await fetch('/api/auto-draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: adminPassword, action, memo, theme: autoTheme })
      })
      const data = await response.json()
      if (!data.success) {
        setAutoError(data.error || '失敗しました')
      } else if (action === 'test') {
        setAutoMessage(data.message)
      } else if (data.status === 'created') {
        setAutoMessage(`下書きを作成しました：「${data.title}」`)
        setAutoEditUrl(data.draft.editUrl)
        setMemo('')
      } else {
        setAutoMessage(data.reason || '作成しませんでした')
      }
    } catch {
      setAutoError('通信エラーが発生しました（生成に時間がかかりすぎた可能性があります。WordPressの下書き一覧も確認してください）')
    } finally {
      setAutoBusy('')
    }
  }

  const handleSaveSettings = useCallback(() => {
    saveSettings(settings)
    setSettingsSaved(true)
    setTimeout(() => setSettingsSaved(false), 2000)
  }, [settings])

  const addRefLink = () => {
    if (newRefLink.trim()) {
      const updated = { ...settings, referenceLinks: [...settings.referenceLinks, newRefLink.trim()] }
      setSettings(updated)
      setNewRefLink('')
      saveSettings(updated)
    }
  }

  const removeRefLink = (index: number) => {
    const updated = { ...settings, referenceLinks: settings.referenceLinks.filter((_, i) => i !== index) }
    setSettings(updated)
    saveSettings(updated)
  }

  const addNgWord = () => {
    if (newNgWord.trim() && !settings.ngWords.includes(newNgWord.trim())) {
      const updated = { ...settings, ngWords: [...settings.ngWords, newNgWord.trim()] }
      setSettings(updated)
      setNewNgWord('')
      saveSettings(updated)
    }
  }

  const removeNgWord = (word: string) => {
    const updated = { ...settings, ngWords: settings.ngWords.filter(w => w !== word) }
    setSettings(updated)
    saveSettings(updated)
  }

  const handleGenerate = async () => {
    if (!settings.blogIndexUrl.trim()) {
      setError('ブログのURLを入力してください')
      return
    }
    setIsGenerating(true)
    setError('')
    setArticle('')
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...settings, customInstruction })
      })
      const data = await response.json()
      if (data.success) {
        setArticle(data.article)
        setActiveTab('generate')
      } else {
        setError(data.error || '記事生成に失敗しました')
      }
    } catch {
      setError('通信エラーが発生しました')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(article)
    setCopyDone(true)
    setTimeout(() => setCopyDone(false), 2000)
  }

  return (
    <div className={styles.root}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <div className={styles.logo}>
            <span className={styles.logoMark}>文</span>
            <div>
              <h1 className={styles.logoTitle}>ブログ記事ジェネレーター</h1>
              <p className={styles.logoSub}>あなたの文体で、新しい記事を</p>
            </div>
          </div>
          <nav className={styles.nav}>
            <button
              className={`${styles.navBtn} ${activeTab === 'generate' ? styles.navActive : ''}`}
              onClick={() => setActiveTab('generate')}
            >生成</button>
            <button
              className={`${styles.navBtn} ${activeTab === 'auto' ? styles.navActive : ''}`}
              onClick={() => setActiveTab('auto')}
            >自動投稿</button>
            <button
              className={`${styles.navBtn} ${activeTab === 'settings' ? styles.navActive : ''}`}
              onClick={() => setActiveTab('settings')}
            >設定</button>
          </nav>
        </div>
      </header>

      <main className={styles.main}>
        {activeTab === 'generate' && (
          <div className={styles.generateLayout}>
            {/* Left panel */}
            <div className={styles.panel}>
              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>📖</span>
                  あなたのブログURL
                  <span className={styles.required}>必須</span>
                </label>
                <p className={styles.hint}>記事一覧ページや代表的な記事のURLを入力してください</p>
                <input
                  type="url"
                  placeholder="https://yourblog.com/posts"
                  value={settings.blogIndexUrl}
                  onChange={e => setSettings({ ...settings, blogIndexUrl: e.target.value })}
                />
              </section>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>🔗</span>
                  参照リンク（任意）
                </label>
                <p className={styles.hint}>引用したい記事や参考にしたい情報源のURLを追加</p>
                <div className={styles.inputRow}>
                  <input
                    type="url"
                    placeholder="https://reference.example.com/article"
                    value={newRefLink}
                    onChange={e => setNewRefLink(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && addRefLink()}
                  />
                  <button className={styles.addBtn} onClick={addRefLink}>追加</button>
                </div>
                {settings.referenceLinks.length > 0 && (
                  <ul className={styles.tagList}>
                    {settings.referenceLinks.map((link, i) => (
                      <li key={i} className={styles.linkTag}>
                        <span className={styles.linkTagText}>{link}</span>
                        <button className={styles.removeBtn} onClick={() => removeRefLink(i)}>×</button>
                      </li>
                    ))}
                  </ul>
                )}
              </section>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>✏️</span>
                  追加指示（任意）
                </label>
                <p className={styles.hint}>テーマや特定のトピックなど、今回の記事への指示</p>
                <textarea
                  rows={3}
                  placeholder="例：今回は「生産性向上」をテーマに、具体的な方法を3つ紹介する記事を書いてください"
                  value={customInstruction}
                  onChange={e => setCustomInstruction(e.target.value)}
                  style={{ resize: 'vertical' }}
                />
              </section>

              {error && <div className={styles.errorBox}>{error}</div>}

              <button
                className={styles.generateBtn}
                onClick={handleGenerate}
                disabled={isGenerating}
              >
                {isGenerating ? (
                  <>
                    <span className={styles.spinner}></span>
                    生成中...
                  </>
                ) : '記事を生成する'}
              </button>
            </div>

            {/* Right panel - output */}
            <div className={styles.outputPanel}>
              {!article && !isGenerating && (
                <div className={styles.emptyState}>
                  <div className={styles.emptyIcon}>📝</div>
                  <p>左側のフォームに情報を入力して<br />「記事を生成する」を押してください</p>
                </div>
              )}

              {isGenerating && (
                <div className={styles.loadingState}>
                  <div className={styles.loadingDots}>
                    <span></span><span></span><span></span>
                  </div>
                  <p>ブログを分析して記事を作成中...</p>
                </div>
              )}

              {article && (
                <>
                  <div className={styles.outputHeader}>
                    <span className={styles.outputTitle}>生成された記事</span>
                    <button className={styles.copyBtn} onClick={handleCopy}>
                      {copyDone ? '✓ コピー完了' : 'コピー'}
                    </button>
                  </div>
                  <div
                    className={`${styles.articleContent} article-output`}
                    dangerouslySetInnerHTML={{ __html: parseMarkdown(article) }}
                  />
                </>
              )}
            </div>
          </div>
        )}

        {activeTab === 'auto' && (
          <div className={styles.settingsLayout}>
            <div className={styles.settingsPanel}>
              <h2 className={styles.settingsTitle}>WordPress 自動下書き</h2>

              <div className={styles.apiKeyNote} style={{ marginBottom: 24 }}>
                <strong>毎日13時ごろ（日本時間）に自動で下書きを作成します</strong>
                <p>曜日ごとのテーマで記事を書き、WordPressに「下書き」として保存します。公開はWordPressの管理画面から行ってください。<br />
                  校舎のできごとがある日は、下の「校舎メモ」から下書きを作ると、その日の自動作成はお休みになります。</p>
              </div>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>🔑</span>
                  パスワード
                  <span className={styles.required}>必須</span>
                </label>
                <p className={styles.hint}>Vercel に設定した ADMIN_PASSWORD（このブラウザに保存されます）</p>
                <input
                  type="password"
                  value={adminPassword}
                  onChange={e => setAdminPassword(e.target.value)}
                />
              </section>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>🏫</span>
                  今日の校舎メモ（任意）
                </label>
                <p className={styles.hint}>書いてあることだけを事実として使います。空欄なら曜日のテーマで書きます</p>
                <textarea
                  rows={5}
                  placeholder={'例：\n・中2の英語小テストで満点が続出\n・10月から冬期講習の申し込み受付開始\n・自習室を平日21時まで開放中'}
                  value={memo}
                  onChange={e => setMemo(e.target.value)}
                  style={{ resize: 'vertical' }}
                />
              </section>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>🎯</span>
                  テーマ指定（任意）
                </label>
                <p className={styles.hint}>メモがないときに、曜日のテーマの代わりに使うテーマ</p>
                <input
                  type="text"
                  placeholder="例：中3の2学期の過ごし方"
                  value={autoTheme}
                  onChange={e => setAutoTheme(e.target.value)}
                />
              </section>

              {autoError && <div className={styles.errorBox}>{autoError}</div>}
              {autoMessage && (
                <div className={styles.apiKeyNote} style={{ marginBottom: 16 }}>
                  <p style={{ margin: 0 }}>{autoMessage}</p>
                  {autoEditUrl && (
                    <p style={{ margin: '8px 0 0' }}>
                      <a href={autoEditUrl} target="_blank" rel="noreferrer">WordPressで下書きを開く →</a>
                    </p>
                  )}
                </div>
              )}

              <button
                className={styles.generateBtn}
                onClick={() => handleAutoDraft('create')}
                disabled={autoBusy !== ''}
              >
                {autoBusy === 'create' ? (
                  <>
                    <span className={styles.spinner}></span>
                    作成中...（1〜2分かかります）
                  </>
                ) : '今すぐ下書きを作成'}
              </button>
              <button
                className={styles.saveBtn}
                style={{ marginTop: 12 }}
                onClick={() => handleAutoDraft('test')}
                disabled={autoBusy !== ''}
              >
                {autoBusy === 'test' ? '確認中...' : 'WordPress接続テスト'}
              </button>
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div className={styles.settingsLayout}>
            <div className={styles.settingsPanel}>
              <h2 className={styles.settingsTitle}>設定</h2>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>🚫</span>
                  NGワード
                </label>
                <p className={styles.hint}>記事内で使用しないようにする言葉を登録してください</p>
                <div className={styles.inputRow}>
                  <input
                    type="text"
                    placeholder="例：〜という感じ"
                    value={newNgWord}
                    onChange={e => setNewNgWord(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && addNgWord()}
                  />
                  <button className={styles.addBtn} onClick={addNgWord}>追加</button>
                </div>
                {settings.ngWords.length > 0 ? (
                  <div className={styles.ngWordGrid}>
                    {settings.ngWords.map(word => (
                      <span key={word} className={styles.ngWord}>
                        {word}
                        <button className={styles.ngRemoveBtn} onClick={() => removeNgWord(word)}>×</button>
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className={styles.emptyHint}>NGワードはまだ登録されていません</p>
                )}
              </section>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>📌</span>
                  記事末尾の定型文
                </label>
                <p className={styles.hint}>すべての記事の最後に自動で追加されるテキスト（プロフィール、SNSリンクなど）</p>
                <textarea
                  rows={6}
                  placeholder={`例：\n---\n最後まで読んでいただきありがとうございます！\n\nTwitter: @youraccount\nお問い合わせはこちら: contact@yourblog.com`}
                  value={settings.closingText}
                  onChange={e => setSettings({ ...settings, closingText: e.target.value })}
                  style={{ resize: 'vertical', fontFamily: 'monospace', fontSize: '13px' }}
                />
              </section>

              <button className={styles.saveBtn} onClick={handleSaveSettings}>
                {settingsSaved ? '✓ 保存しました' : '設定を保存'}
              </button>

              <div className={styles.apiKeyNote}>
                <strong>APIキーの設定について</strong>
                <p>このアプリを動かすには Anthropic API キーが必要です。<br />
                  Vercel にデプロイする際は、環境変数 <code>ANTHROPIC_API_KEY</code> を設定してください。</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
