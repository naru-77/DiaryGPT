# Diary

インタービューから自動日記生成アプリ

# 初期手順を簡略化しました！！！！！

### 初期設定が終わったらいつもやること

bash setup.sh #venv使う人向け

python app.py

あとは新規登録してログインすれば使えます！

### 初期設定

ルートディレクトリ直下に.env ファイルを作り、以下を記入。
OPENAI_API_KEY=your_api_key

## メモ

※いきなり 403 になったら、キャッシュ削除してみる

## 毎回起動時に行うこと?

### 2 つ目の venv は仮想環境の名前

python3 -m venv venv

### この venv も仮想環境の名前

source venv/bin/activate

### pip の version アップデート

/Users/r.nishino/DiaryGPT/venv/bin/python3 -m pip install --upgrade pip

### 環境変数を設定
以下を.envに追加

export OPENAI_API_KEY=''

export STABILITY_SDK_API_KEY=''

### 必要ライブラリ

- flask
- pytz
- sqlite3
- flask_sqlalchemy
- flask_login
- openai
- stability_sdk

### db の初期化手順

1. instance 直下の blog.db を削除
1. "prepare_db.py"を実行


### 絵の生成について
stability-sdkを使いました

https://dreamstudio.ai/account
このurlに行って、アカウントを作成し、APIキーを取得する必要があります。
後は、stability_sdkをインストールすれば使えます。
