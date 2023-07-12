from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime  
import pytz
import os
import openai

# ここからDB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Post(db.Model): # データベースのテーブル
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')).replace(second=0, microsecond=0))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST']) # 最初の画面
def home():
    if request.method == 'GET':
        posts = Post.query.all()

    return render_template('home.html', posts=posts)

@app.route('/create', methods=['GET','POST']) # 新規作成画面
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/<int:id>/update', methods=['GET','POST']) # 編集ボタン
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)    
    else:
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        db.session.commit()
        return redirect('/')
    
@app.route('/<int:id>/delete', methods=['GET']) # 削除ボタン
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/<int:id>/contents', methods=['GET']) # コンテンツ詳細表示
def contents(id):
    post = Post.query.get(id)
    return render_template('contents.html', post=post)    



# ここからGPT

openai.api_key = os.getenv('OPENAI_API_KEY') # 以降のopenaiライブラリにはこのAPIを用いる

# メッセージを保存するリスト
messages = [
    {"role": "system", "content": "あなたは日記を作るためのインタビュアーです。短い質問を1つだけしてください。"},
    {"role": "system", "content": "最初は「今日はどんな一日でしたか？」という質問をしました。"},
]


def query_chatgpt(prompt): # 質問を生成する
    # ユーザーのメッセージをリストに追加
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # GPTの応答をリストに追加
    gpt_response = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": gpt_response})

    return gpt_response

def summary_chatgpt(prompt): # 日記をまとめる

    prompt.append({"role": "user", "content": "以上の情報を用いて、日記を作成してください。100字くらいの文章で、見やすさと分かりやすさに気をつけてください。"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )

    # GPTの応答をリストに追加
    gpt_response = response.choices[0].message.content.strip()

    return gpt_response

def title_chatgpt(prompt): # タイトルをつける

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "以下の情報を用いて、日記のタイトルを書いてください。10文字程度の体言止めで、見やすさと分かりやすさに気をつけて作ってください。"},{"role": "user", "content": prompt}]
    )

    # GPTの応答をリストに追加
    gpt_response = response.choices[0].message.content.strip()

    return gpt_response


@app.route('/gpt', methods=['POST']) # 質問を作る
def gpt():
    try:
        prompt = request.form.get('speech')
        response = query_chatgpt(prompt)
        return response, 200
    except Exception as e:
        return str(e), 500
    

@app.route('/summary', methods=['POST']) # 日記を作る
def summary():
    global messages  # messages をグローバル変数として宣言
    inputText = request.form.get('inputText')
    messages.append({"role": "user", "content": inputText})

    diary_messages = messages[1:]  # 日記作成に使用するメッセージを取得（最初のシステムメッセージを除く）
    diary_response = summary_chatgpt(diary_messages) # 日記を作成
    diary_title = title_chatgpt(diary_response) # タイトル生成

    messages = [
        {"role": "system", "content": "あなたは日記を作るためのインタビュアーです。短い質問を1つだけしてください。"},
        {"role": "system", "content": "最初は「今日はどんな一日でしたか？」という質問をしました。"},
        ] # GPTの記憶をリセット
        
    post = Post(title=diary_title, body=diary_response)
    db.session.add(post)
    db.session.commit()
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)