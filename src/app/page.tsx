'use client'

import { useState, useEffect, useCallback } from 'react'
import { FixedImage, ImagePosition, Settings, WordPressDraftResponse } from '@/types'
import { defaultSettings, loadSettings, saveSettings } from '@/lib/settings'
import { buildArticleHtml, buildArticleMarkdown, markdownToHtml, splitTitle } from '@/lib/markdown'
import { normalizeSiteUrl } from '@/lib/wordpress'
import styles from './page.module.css'

const MAX_IMAGE_SIZE = 1600

// アップロードされた画像を縮小して data URL にする（ブラウザ保存容量を節約するため）
function fileToDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onerror = () => reject(new Error('画像を読み込めませんでした'))
    reader.onload = () => {
      const original = reader.result as string
      if (file.type === 'image/gif') return resolve(original)
      const img = new Image()
      img.onerror = () => reject(new Error('画像を読み込めませんでした'))
      img.onload = () => {
        const scale = Math.min(1, MAX_IMAGE_SIZE / Math.max(img.width, img.height))
        const canvas = document.createElement('canvas')
        canvas.width = Math.round(img.width * scale)
        canvas.height = Math.round(img.height * scale)
        const ctx = canvas.getContext('2d')
        if (!ctx) return resolve(original)
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
        resolve(canvas.toDataURL('image/jpeg', 0.85))
      }
      img.src = original
    }
    reader.readAsDataURL(file)
  })
}

export default function Home() {
  const [settings, setSettings] = useState<Settings>(defaultSettings)
  const [newRefLink, setNewRefLink] = useState('')
  const [newNgWord, setNewNgWord] = useState('')
  const [customInstruction, setCustomInstruction] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [article, setArticle] = useState('')
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState<'generate' | 'settings'>('generate')
  const [settingsSaved, setSettingsSaved] = useState(false)
  const [copyDone, setCopyDone] = useState(false)
  const [newImageUrl, setNewImageUrl] = useState('')
  const [newImageAlt, setNewImageAlt] = useState('')
  const [newImagePosition, setNewImagePosition] = useState<ImagePosition>('bottom')
  const [imageError, setImageError] = useState('')
  const [wpTestState, setWpTestState] = useState<{ status: 'idle' | 'testing' | 'ok' | 'error'; message: string }>({ status: 'idle', message: '' })
  const [isSendingWp, setIsSendingWp] = useState(false)
  const [wpResult, setWpResult] = useState<WordPressDraftResponse | null>(null)

  useEffect(() => {
    setSettings(loadSettings())
  }, [])

  const handleSaveSettings = useCallback(() => {
    if (!saveSettings(settings)) {
      setImageError('設定を保存できませんでした。画像の枚数を減らすか、画像URLでの登録をお試しください')
      return
    }
    setSettingsSaved(true)
    setTimeout(() => setSettingsSaved(false), 2000)
  }, [settings])

  const updateImages = (fixedImages: FixedImage[]) => {
    const updated = { ...settings, fixedImages }
    if (!saveSettings(updated)) {
      setImageError('画像を保存できませんでした（ブラウザの保存容量の上限です）。画像の枚数を減らすか、画像URLでの登録をお試しください')
      return false
    }
    setImageError('')
    setSettings(updated)
    return true
  }

  const createImage = (src: string): FixedImage => ({
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    src,
    alt: newImageAlt.trim(),
    position: newImagePosition
  })

  const addImageUrl = () => {
    const url = newImageUrl.trim()
    if (!url) return
    if (!/^https?:\/\//i.test(url)) {
      setImageError('画像URLは http:// または https:// から始まる形式で入力してください')
      return
    }
    if (updateImages([...settings.fixedImages, createImage(url)])) {
      setNewImageUrl('')
      setNewImageAlt('')
    }
  }

  const addImageFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return
    try {
      const added: FixedImage[] = []
      for (const file of Array.from(files)) {
        if (!file.type.startsWith('image/')) continue
        added.push(createImage(await fileToDataUrl(file)))
      }
      if (added.length && updateImages([...settings.fixedImages, ...added])) setNewImageAlt('')
    } catch (e) {
      setImageError(e instanceof Error ? e.message : '画像を読み込めませんでした')
    }
  }

  const removeImage = (id: string) => {
    updateImages(settings.fixedImages.filter(i => i.id !== id))
  }

  const changeImage = (id: string, patch: Partial<FixedImage>) => {
    updateImages(settings.fixedImages.map(i => (i.id === id ? { ...i, ...patch } : i)))
  }

  const moveImage = (id: string, direction: -1 | 1) => {
    const list = [...settings.fixedImages]
    const index = list.findIndex(i => i.id === id)
    const target = index + direction
    if (index < 0 || target < 0 || target >= list.length) return
    ;[list[index], list[target]] = [list[target], list[index]]
    updateImages(list)
  }

  const handleTestWordPress = async () => {
    setWpTestState({ status: 'testing', message: '' })
    try {
      const response = await fetch('/api/wordpress/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wordpress: settings.wordpress })
      })
      const data = await response.json()
      if (data.success) {
        saveSettings(settings)
        setWpTestState({ status: 'ok', message: `接続成功：${data.name} としてログインできました` })
      } else {
        setWpTestState({ status: 'error', message: data.error || '接続に失敗しました' })
      }
    } catch {
      setWpTestState({ status: 'error', message: '通信エラーが発生しました' })
    }
  }

  const handleSendToWordPress = async () => {
    setIsSendingWp(true)
    setWpResult(null)
    const site = normalizeSiteUrl(settings.wordpress.siteUrl)
    const { title, body } = splitTitle(article)
    try {
      const response = await fetch('/api/wordpress/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          wordpress: settings.wordpress,
          title,
          content: markdownToHtml(body),
          images: settings.fixedImages.map(i => ({
            id: i.id,
            // 同じサイトへアップロード済みの画像は再利用する
            src: i.wpMediaUrl && i.wpMediaSite === site ? i.wpMediaUrl : i.src,
            alt: i.alt,
            position: i.position
          }))
        })
      })
      const data: WordPressDraftResponse = await response.json()
      const uploaded = data.uploadedImages || {}
      if (Object.keys(uploaded).length) {
        updateImages(settings.fixedImages.map(i =>
          uploaded[i.id] ? { ...i, wpMediaUrl: uploaded[i.id], wpMediaSite: site } : i
        ))
      }
      setWpResult(data.success ? data : { success: false, error: data.error || 'WordPressへの送信に失敗しました' })
    } catch {
      setWpResult({ success: false, error: '通信エラーが発生しました' })
    } finally {
      setIsSendingWp(false)
    }
  }

  const wpConfigured = Boolean(
    settings.wordpress.siteUrl.trim() && settings.wordpress.username.trim() && settings.wordpress.appPassword.trim()
  )

  const updateWordPress = (patch: Partial<Settings['wordpress']>) => {
    setSettings({ ...settings, wordpress: { ...settings.wordpress, ...patch } })
    setWpTestState({ status: 'idle', message: '' })
  }

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
    setWpResult(null)
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
    navigator.clipboard.writeText(buildArticleMarkdown(article, settings.fixedImages))
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
                    <div className={styles.outputActions}>
                      <button className={styles.copyBtn} onClick={handleCopy}>
                        {copyDone ? '✓ コピー完了' : 'コピー'}
                      </button>
                      <button
                        className={styles.wpBtn}
                        onClick={wpConfigured ? handleSendToWordPress : () => setActiveTab('settings')}
                        disabled={isSendingWp}
                        title={wpConfigured ? 'WordPressに下書きとして保存します' : '設定タブでWordPressの接続情報を入力してください'}
                      >
                        {isSendingWp ? '送信中...' : wpConfigured ? 'WordPressに下書き保存' : 'WordPress連携を設定'}
                      </button>
                    </div>
                  </div>
                  {wpResult && (
                    <div className={wpResult.success ? styles.wpSuccess : styles.wpError}>
                      {wpResult.success ? (
                        <>
                          ✓ WordPressに下書きを保存しました
                          <a href={wpResult.editUrl} target="_blank" rel="noreferrer">編集画面を開く</a>
                          <a href={wpResult.previewUrl} target="_blank" rel="noreferrer">プレビュー</a>
                        </>
                      ) : wpResult.error}
                    </div>
                  )}
                  <div
                    className={`${styles.articleContent} article-output`}
                    dangerouslySetInnerHTML={{ __html: buildArticleHtml(article, settings.fixedImages) }}
                  />
                </>
              )}
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

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>🖼️</span>
                  固定画像
                </label>
                <p className={styles.hint}>すべての記事に自動で入れる写真（プロフィール写真、バナーなど）。記事の冒頭（タイトル直後）か末尾を選べます</p>
                <div className={styles.imageForm}>
                  <div className={styles.inputRow}>
                    <select
                      value={newImagePosition}
                      onChange={e => setNewImagePosition(e.target.value as ImagePosition)}
                      className={styles.positionSelect}
                    >
                      <option value="top">記事の冒頭</option>
                      <option value="bottom">記事の末尾</option>
                    </select>
                    <input
                      type="text"
                      placeholder="代替テキスト（任意）例：筆者のプロフィール写真"
                      value={newImageAlt}
                      onChange={e => setNewImageAlt(e.target.value)}
                    />
                  </div>
                  <div className={styles.inputRow}>
                    <input
                      type="url"
                      placeholder="画像URL（https://...）"
                      value={newImageUrl}
                      onChange={e => setNewImageUrl(e.target.value)}
                      onKeyDown={e => e.key === 'Enter' && addImageUrl()}
                    />
                    <button className={styles.addBtn} onClick={addImageUrl}>URLで追加</button>
                    <label className={styles.addBtn}>
                      画像を選択
                      <input
                        type="file"
                        accept="image/*"
                        multiple
                        hidden
                        onChange={e => {
                          addImageFiles(e.target.files)
                          e.target.value = ''
                        }}
                      />
                    </label>
                  </div>
                </div>
                {imageError && <div className={styles.errorBox}>{imageError}</div>}
                {settings.fixedImages.length > 0 ? (
                  <ul className={styles.imageList}>
                    {settings.fixedImages.map((image, i) => (
                      <li key={image.id} className={styles.imageItem}>
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img src={image.src} alt={image.alt} className={styles.imageThumb} />
                        <div className={styles.imageFields}>
                          <select
                            value={image.position}
                            onChange={e => changeImage(image.id, { position: e.target.value as ImagePosition })}
                            className={styles.positionSelect}
                          >
                            <option value="top">記事の冒頭</option>
                            <option value="bottom">記事の末尾</option>
                          </select>
                          <input
                            type="text"
                            placeholder="代替テキスト"
                            value={image.alt}
                            onChange={e => changeImage(image.id, { alt: e.target.value })}
                          />
                        </div>
                        <div className={styles.imageActions}>
                          <button className={styles.moveBtn} onClick={() => moveImage(image.id, -1)} disabled={i === 0} aria-label="上へ">↑</button>
                          <button className={styles.moveBtn} onClick={() => moveImage(image.id, 1)} disabled={i === settings.fixedImages.length - 1} aria-label="下へ">↓</button>
                          <button className={styles.removeBtn} onClick={() => removeImage(image.id)} aria-label="削除">×</button>
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className={styles.emptyHint}>固定画像はまだ登録されていません</p>
                )}
              </section>

              <section className={styles.section}>
                <label className={styles.label}>
                  <span className={styles.labelIcon}>📝</span>
                  WordPress連携
                </label>
                <p className={styles.hint}>
                  生成した記事をボタンひとつでWordPressの下書きに保存できます。<br />
                  パスワードはログイン用ではなく、WordPress管理画面の「ユーザー → プロフィール → アプリケーションパスワード」で発行したものを入力してください
                </p>
                <input
                  type="url"
                  placeholder="サイトURL（例：https://yourblog.com）"
                  value={settings.wordpress.siteUrl}
                  onChange={e => updateWordPress({ siteUrl: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="ユーザー名"
                  autoComplete="off"
                  value={settings.wordpress.username}
                  onChange={e => updateWordPress({ username: e.target.value })}
                />
                <input
                  type="password"
                  placeholder="アプリケーションパスワード（xxxx xxxx xxxx xxxx xxxx xxxx）"
                  autoComplete="new-password"
                  value={settings.wordpress.appPassword}
                  onChange={e => updateWordPress({ appPassword: e.target.value })}
                />
                <div className={styles.wpTestRow}>
                  <button
                    className={styles.addBtn}
                    onClick={handleTestWordPress}
                    disabled={!wpConfigured || wpTestState.status === 'testing'}
                  >
                    {wpTestState.status === 'testing' ? '接続確認中...' : '接続テスト'}
                  </button>
                  {wpTestState.message && (
                    <span className={wpTestState.status === 'ok' ? styles.wpTestOk : styles.wpTestError}>
                      {wpTestState.message}
                    </span>
                  )}
                </div>
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
