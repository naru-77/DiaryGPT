from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import datetime  
from datetime import timedelta
import pytz
import os
import openai
from flask_login import UserMixin, LoginManager, login_user,logout_user, login_required # flask_loginのインストールが必要
from werkzeug.security import generate_password_hash, check_password_hash

openai.api_key = "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" # 以降のopenaiライブラリにはこのAPIを用いる


def query_chatgpt(prompt): # gptを使うための関数
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "あなたはインタビュアーです。最初は「今日はどんな一日でしたか？」という質問をしました。回答に応じて、よりその話題について深ぼることのできる質問をしてください。質問は簡潔に1つです。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24) # セッション情報の暗号化のためシークレットキーをランダム生成
db = SQLAlchemy(app)

login_manager = LoginManager() # LoginManagerをインスタンス化
login_manager.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)  # ユーザー名
    post_id = db.Column(db.Integer, nullable=False)  # 投稿ID
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')).replace(second=0, microsecond=0))  # 時間の秒以下を無視

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(12))
    post_count = db.Column(db.Integer, default=0)  # 投稿数を管理するカラム
    
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)  
    
    
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
        user = User.query.filter_by(username=username).first()
        user.post_count = user.post_count + 1
        db.session.commit()
        post = Post(username=username ,post_id=user.post_count,title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/{username}')
    else:
        return render_template('create.html', username=username)

@app.route('/<username>/<int:post_id>/update', methods=['GET','POST']) # ユーザー専用編集
@login_required # アクセス制限
def update(post_id,username):
    posts = Post.query.filter_by(username=username).first()
    if(posts != None):
        post = posts.query.get(post_id)
    
        if request.method == 'GET':
            return render_template('update.html', post=post)    
        else:
            post.title = request.form.get('title')
            post.body = request.form.get('body')

            db.session.commit()
            return redirect(f'/{username}')
    
@app.route('/<username>/<int:post_id>/delete', methods=['GET']) # ユーザー専用削除
@login_required # アクセス制限
def delete(post_id,username):
    posts = Post.query.filter_by(username=username).first()
    user = User.query.filter_by(username=username).first()
    if(posts != None):
        post = posts.query.get(post_id)
        user.post_count = user.post_count - 1
        db.session.delete(post)
        db.session.commit()
        return redirect(f'/{username}')

@app.route('/<username>/<int:post_id>/contents', methods=['GET']) # ユーザー専用コンテンツ詳細表示
def contents(post_id,username):
    user = User.query.filter_by(username=username).first() # ユーザー名でフィルターをかける
    if(post_id==0):
        return redirect(f'/{username}/{user.post_count}/contents')
    elif(post_id==user.post_count+1):
        return redirect(f'/{username}/{1}/contents')  
    else:
        post = Post.query.filter_by(username=username, post_id=post_id).first()
        return render_template('contents.html', post=post, username=username)


@app.route('/speech', methods=['POST']) # 音声入力のエンドポイント
def speech():
    text = request.form.get('speech')  # 音声テキストを取得
    return text, 200

@app.route('/gpt', methods=['POST']) # gptのエンドポイント
def gpt():
    try:
        prompt = request.form.get('prompt')
        response = query_chatgpt(prompt)
        return response, 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)

