# ブログ記事ジェネレーター

あなたのブログの文体を学習して、新しいブログ記事を自動生成するアプリです。

## 機能

- 📖 **ブログURL読み取り** - あなたのブログを解析して文体・スタイルを学習
- 🔗 **参照リンク追加** - 引用したい記事を個別に追加可能
- 🚫 **NGワード管理** - 使用したくない言葉を蓄積・管理
- 📌 **定型文設定** - 記事末尾に自動挿入するテキストを設定

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/blog-generator.git
cd blog-generator
```

### 2. 依存関係をインストール

```bash
npm install
```

### 3. 環境変数を設定

`.env.local.example` をコピーして `.env.local` を作成し、APIキーを設定します：

```bash
cp .env.local.example .env.local
```

`.env.local` を編集：
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Anthropic APIキーは https://console.anthropic.com/ で取得できます。

### 4. 開発サーバーを起動

```bash
npm run dev
```

http://localhost:3000 でアプリが起動します。

## Vercelへのデプロイ

### 方法1: Vercel CLIを使う

```bash
npm i -g vercel
vercel
```

### 方法2: GitHubと連携

1. このリポジトリをGitHubにプッシュ
2. [Vercel](https://vercel.com) でGitHubと連携してインポート
3. 環境変数 `ANTHROPIC_API_KEY` を設定
4. デプロイ実行

### 環境変数の設定（Vercel）

Vercelダッシュボード → プロジェクト → Settings → Environment Variables で以下を追加：

| 変数名 | 値 |
|--------|-----|
| `ANTHROPIC_API_KEY` | Anthropicのコンソールで取得したAPIキー |

## 技術スタック

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **AI**: Anthropic Claude API
- **Scraping**: Cheerio
- **Deploy**: Vercel

## 使い方

1. **「設定」タブ**でNGワードと定型文を設定・保存
2. **「生成」タブ**であなたのブログURLを入力
3. 必要に応じて参照リンクや追加指示を入力
4. 「記事を生成する」ボタンをクリック
5. 生成された記事をコピーして使用

## WordPress 自動下書き（毎日）

毎日 **13時ごろ（日本時間）** に Vercel Cron が `/api/cron/daily-draft` を呼び出し、記事を生成して WordPress に **下書き** として保存します。公開は WordPress の管理画面から手動で行います。

- テーマ：校舎メモがあればそれを中心に、なければ曜日ごとのテーマ（`src/config/autoPost.ts`）
- SEO：地域キーワード・見出し構成・スラッグ・抜粋（メタディスクリプション）・タグを自動設定
- 文体：WordPress の最近の公開記事3本を参考にし、最近のタイトルと重複しないようにする
- 今日すでに自動下書き（「自動投稿」タブから作ったものを含む）がある場合、その日の定期実行はスキップ
- 確認が必要な情報には本文中に【要確認】が付きます

### 必要な環境変数（Vercel → Settings → Environment Variables）

| 変数名 | 内容 |
|--------|------|
| `WP_BASE_URL` | `https://meiseikobetsu.jp` |
| `WP_USERNAME` | WordPress のユーザー名 |
| `WP_APP_PASSWORD` | WordPress「ユーザー → プロフィール → アプリケーションパスワード」で発行したもの |
| `WP_CATEGORY_IDS` | （任意）下書きに付けるカテゴリーID（カンマ区切り） |
| `ADMIN_PASSWORD` | アプリの「自動投稿」タブで使うパスワード（自分で決める） |
| `CRON_SECRET` | 定期実行の認証用のランダムな長い文字列 |
| `ANTHROPIC_MODEL` | （任意）使うモデル。未設定なら `claude-opus-4-5` |

### テーマ・キーワード・末尾の定型文を変える

`src/config/autoPost.ts` を編集してプッシュしてください。
