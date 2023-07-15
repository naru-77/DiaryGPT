#!/bin/bash

# 'venv'ディレクトリが存在すれば削除
if [ -d "venv" ]; then
  rm -r venv
fi

# Pythonの仮想環境を作成
python3 -m venv venv

# 仮想環境をアクティベート
source venv/bin/activate

# pipをアップグレード
python3 -m pip install --upgrade pip

# 必要なパッケージをインストール
pip install -r requirements-for-setup.txt

# dbの初期化
# 'instance'ディレクトリが存在すれば削除
if [ -d "instance" ]; then
  rm -r instance
fi
python prepare_db.py