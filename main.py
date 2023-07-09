from flask import *
import os
import openai
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

@app.route('/') # 最初の画面
def home():
    return render_template('home.html')

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

