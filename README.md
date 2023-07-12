# Diary

日記アプリ

# いきなり 403 になったら、キャッシュ削除してみる

# 毎回起動時に行うこと?(れん)

# 2 つ目の venv は仮想環境の名前

python3 -m venv venv

# この venv も仮想環境の名前

source venv/bin/activate

pip install flask

# pip の version アップデート

/Users/r.nishino/DiaryGPT/venv/bin/python3 -m pip install --upgrade pip

pip install openai

# 環境変数を設定

export OPENAI_API_KEY=''

## 必要ライブラリ
flask

sqlite3

flask_sqlalchemy

flask_login

## dbの初期化手順
1. instance直下のblog.dbを削除
1. "prepare_db.py"を実行
