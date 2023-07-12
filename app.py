from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime  
import pytz
import os
import openai
from flask_login import UserMixin, LoginManager, login_user,logout_user, login_required # flask_loginのインストールが必要
from werkzeug.security import generate_password_hash, check_password_hash

openai.api_key = os.getenv('OPENAI_API_KEY') # 以降のopenaiライブラリにはこのAPIを用いる

# ここからDB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24) # セッション情報の暗号化のためシークレットキーをランダム生成
db = SQLAlchemy(app)

login_manager = LoginManager() # LoginManagerをインスタンス化
login_manager.init_app(app)

class Post(db.Model): # データベースのテーブル
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True) # usernameをデータベースに追加
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')).replace(second=0, microsecond=0)) # 時間の秒以下を無視
    

    
class User(UserMixin, db.Model): # ユーザーのテーブル
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(12))
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ユーザー専用ホーム
@app.route('/<username>', methods=['GET', 'POST'])
@login_required # アクセス制限
def home(username):
    if request.method == 'GET':
        posts = Post.query.filter_by(username=username).all() # ユーザーネームが等しいものをすべて取得

        return render_template('home.html', posts=posts, username=username)
    else:
        posts = Post.query.filter_by(username=username).all() # ユーザーネームが等しいものをすべて取得
        return render_template('home.html', posts=posts, username=username)


@app.route('/signup', methods=['GET','POST']) # サインアップ画面
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='sha256')) # ユーザーをインスタンス化、この時パスワードをハッシュ化
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET','POST']) # ログイン画面
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first() # ユーザー名でフィルターをかける
        if check_password_hash(user.password,password): # ハッシュ化されたパスワードと比較
            login_user(user)
            return redirect(f'/{username}')
        
    else:
        return render_template('login.html')

# ログアウト
@app.route('/logout')
@login_required # アクセス制限
def logout():
    logout_user()
    return redirect('/login')


@app.route('/<username>/create', methods=['GET','POST']) #ユーザー専用新規作成画面
@login_required # アクセス制限
def create(username):
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(username=username ,title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/{username}')
    else:
        return render_template('create.html', username=username)

@app.route('/<username>/<int:id>/update', methods=['GET','POST']) # ユーザー専用編集
@login_required # アクセス制限
def update(id,username):
    user = Post.query.filter_by(username=username).first()
    if(user != None):
        post = user.query.get(id)
    
        if request.method == 'GET':
            return render_template('update.html', post=post)    
        else:
            post.title = request.form.get('title')
            post.body = request.form.get('body')

            db.session.commit()
            return redirect(f'/{username}')
    
@app.route('/<username>/<int:id>/delete', methods=['GET']) # ユーザー専用削除
@login_required # アクセス制限
def delete(id,username):
    user = Post.query.filter_by(username=username).first()
    if(user != None):
        post = user.query.get(id)

        db.session.delete(post)
        db.session.commit()
        return redirect(f'/{username}')

@app.route('/<username>/<int:id>/contents', methods=['GET']) # ユーザー専用コンテンツ詳細表示
def contents(id,username):
    user = Post.query.filter_by(username=username).first()
    if(user != None):
        post = user.query.get(id)
        return render_template('contents.html', post=post, username=username)    


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


@app.route('/<username>/summary', methods=['POST']) # 日記を作る
def summary(username):
    global messages  # messages をグローバル変数として宣言
    prompt = request.form.get('prompt')
    messages.append({"role": "user", "content": prompt})

    diary_messages = messages[1:]  # 日記作成に使用するメッセージを取得（最初のシステムメッセージを除く）
    diary_response = summary_chatgpt(diary_messages) # 日記を作成
    diary_title = title_chatgpt(diary_response) # タイトル生成

    messages = [
        {"role": "system", "content": "あなたは日記を作るためのインタビュアーです。短い質問を1つだけしてください。"},
        {"role": "system", "content": "最初は「今日はどんな一日でしたか？」という質問をしました。"},
        ] # GPTの記憶をリセット
        
    post = Post(username=username,title=diary_title, body=diary_response)
    db.session.add(post)
    db.session.commit()
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)