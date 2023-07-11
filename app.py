from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime  
import pytz
import os
import openai
from flask_login import UserMixin, LoginManager, login_user,logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

openai.api_key = os.getenv('OPENAI_API_KEY') # 以降のopenaiライブラリにはこのAPIを用いる


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
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Post(db.Model): # データベースのテーブル
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(pytz.timezone('Asia/Tokyo')).replace(second=0, microsecond=0))
    

    
class User(UserMixin, db.Model): # ユーザーのテーブル
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(12))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    

@app.route('/', methods=['GET','POST']) # 最初の画面
@login_required # アクセス制限
def home():
    if request.method == 'GET':
        posts = Post.query.all()

    return render_template('home.html', posts=posts)

@app.route('/signup', methods=['GET','POST']) # サインアップ画面
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='sha256'))
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
        if check_password_hash(user.password,password):
            login_user(user)
            return redirect('/')
        
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required # アクセス制限
def logout():
    logout_user()
    return redirect('/login')


@app.route('/create', methods=['GET','POST']) # 新規作成画面
@login_required # アクセス制限
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
@login_required # アクセス制限
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
@login_required # アクセス制限
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/<int:id>/contents', methods=['GET']) # コンテンツ詳細表示
def contents(id):
    post = Post.query.get(id)
    return render_template('contents.html', post=post)    

    


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

