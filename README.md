# 英語講師サイト（骨組み）

Python (FastAPI) バックエンド + React (Vite) フロントエンドの構成です。

## 構成

- `backend/` — FastAPI。プロフィール・商品・実績のデータ提供、お問い合わせ受付API
- `frontend/` — React (Vite)。自己紹介・商品紹介・実績・お問い合わせの4ページ

## 起動方法

### バックエンド

PowerShell の場合、コマンドは1行ずつ実行してください（`&&` は使えません）。

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

#### お問い合わせ通知メールの設定

お問い合わせフォームが送信されると `masa09english@gmail.com` 宛にメール通知が届くようになっています。
送信には [Resend](https://resend.com)（無料枠あり、クレジットカード不要）のAPIキーが必要です。
SMTP（Gmailアプリパスワードなど）は使っていません — RenderなどのPaaS無料プランはSMTPポートの通信がブロック/ハングすることが多く、確実に送信できないためです。

```powershell
cd backend
copy .env.example .env
```

`.env` を開いて `RESEND_API_KEY` を実際のAPIキーに書き換えてください。
未設定のままでもフォーム送信自体は失敗せず、サーバーのログに「送信をスキップしました」と出るだけです。

`.\venv\Scripts\python.exe` を直接指定する方法なら、`Activate.ps1` の
スクリプト実行ポリシーの問題や `pip.exe` の実行権限エラーを回避できます。
（`Activate.ps1` で有効化したい場合は事前に
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` が必要です。）

### フロントエンド

```
cd frontend
npm install
npm run dev
```

`http://localhost:5173` にアクセス。`/api/*` へのリクエストは Vite の proxy 設定で `http://localhost:8000` に転送されます。

## デプロイ手順（無料構成）

フロントエンドは Vercel、バックエンドは Render の無料プランでリリースする想定です。
コストはドメイン代（任意）以外ゼロで運用できます。

### 0. GitHub にリポジトリを作成してpush

Render・Vercel とも GitHub 連携でのデプロイが最も簡単です。

```powershell
git init
git add .
git commit -m "Initial commit"
```

GitHub で空リポジトリを作成し、指示されたリモート追加・push コマンドを実行してください。

### 1. バックエンド（Render）

1. https://render.com にサインアップ（GitHub連携）
2. 「New +」→「Blueprint」→ このリポジトリを選択（リポジトリ直下の `render.yaml` を自動検出）
3. 環境変数を設定
   - `FRONTEND_ORIGINS` … 後述のVercelのURL（例: `https://your-site.vercel.app`）※フロントエンドを先にデプロイしてから設定でも可
   - `CONTACT_NOTIFY_EMAIL` … 通知を受け取りたいメールアドレス
   - `RESEND_API_KEY` … [resend.com](https://resend.com) で発行したAPIキー（未設定でもフォーム送信自体は失敗しない）
4. デプロイ完了後に発行される URL（例: `https://english-teacher-site-api.onrender.com`）を控える

**無料プランの制約:** 一定時間アクセスがないとスリープし、次のリクエストで初回30〜50秒程度の遅延が発生します。この規模のサイトであれば許容範囲です。

### 2. フロントエンド（Vercel）

1. https://vercel.com にサインアップ（GitHub連携）
2. 「Add New」→「Project」→ このリポジトリを選択
3. 設定
   - Root Directory: `frontend`
   - Framework Preset: Vite（自動検出）
   - Build Command: `npm run build`（デフォルトのままでOK）
   - Output Directory: `dist`（デフォルトのままでOK）
4. 環境変数を設定
   - `VITE_API_BASE_URL` … Renderで発行されたバックエンドURL
   - `VITE_GA_MEASUREMENT_ID` … 下記アクセス解析の測定ID
5. デプロイ

デプロイ後に発行される URL を、Render側の `FRONTEND_ORIGINS` に設定して再デプロイしてください（CORSエラー防止のため）。

### 3. アクセス解析（Google Analytics 4・無料）

1. https://analytics.google.com でアカウント/プロパティを作成
2. 「データストリーム」→ウェブ→サイトURLを登録し、測定ID（`G-XXXXXXXXXX`）を取得
3. Vercel の環境変数 `VITE_GA_MEASUREMENT_ID` に設定して再デプロイ

未設定の場合、解析タグは読み込まれません（`frontend/src/analytics.js`）。

## 今後の拡張案

- お問い合わせデータを DB（SQLite など）に永続化
- プロフィール写真・商品画像のアップロード機能
- 独自ドメインの設定（Vercel/Renderどちらも無料で設定可能）
