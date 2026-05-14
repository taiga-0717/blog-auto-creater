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
