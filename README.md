# ブログ記事ジェネレーター

あなたのブログの文体を学習して、新しいブログ記事を自動生成するアプリです。

## 機能

- 📖 **ブログURL読み取り** - あなたのブログを解析して文体・スタイルを学習
- 🔗 **参照リンク追加** - 引用したい記事を個別に追加可能
- 🚫 **NGワード管理** - 使用したくない言葉を蓄積・管理
- 📌 **定型文設定** - 記事末尾に自動挿入するテキストを設定
- 🖼️ **固定画像** - すべての記事の冒頭（タイトル直後）または末尾に自動で入れる写真を登録
- 📝 **WordPress連携** - 生成した記事をボタンひとつでWordPressの下書きに保存

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

## WordPress連携の設定

1. WordPress管理画面の **ユーザー → プロフィール → アプリケーションパスワード** で、新しいパスワードを発行します（WordPress 5.6以降・HTTPSのサイトで利用可能）
2. このアプリの「設定」タブで、サイトURL・ユーザー名・発行したアプリケーションパスワードを入力し、「接続テスト」で確認します
3. 記事生成後に表示される「WordPressに下書き保存」ボタンを押すと、下書きとして投稿されます
   - 記事の先頭の見出し（`# タイトル`）が投稿タイトルになります
   - アップロードした固定画像はメディアライブラリに自動で登録されます（2回目以降は登録済みの画像を再利用）

※ 接続情報はブラウザ（localStorage）にのみ保存されます。共用のPCでは利用しないでください。

## 使い方

1. **「設定」タブ**でNGワード・定型文・固定画像・WordPress連携を設定・保存
2. **「生成」タブ**であなたのブログURLを入力
3. 必要に応じて参照リンクや追加指示を入力
4. 「記事を生成する」ボタンをクリック
5. 生成された記事をコピーするか、「WordPressに下書き保存」で直接下書きに送信
