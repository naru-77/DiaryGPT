//音声入力ボタンを取得
const button =  document.getElementById("speak-button");
//会話を追記していく領域を取得
const conversation = document.querySelector("#conversation");
let endOnNextQuestion = false; //次の質問で終了するかどうか

function endQuestioning() {
  //終了ボタンを押したら実行
  endOnNextQuestion = !endOnNextQuestion; // ボタンの状態を反転

  // ボタンの色を変更
  document.getElementById("end-button").classList.toggle("btn-danger");

  console.log(endOnNextQuestion);
}

function addUserText(text) {
  //ユーザの回答を表示する関数
  const userDiv = document.createElement("div");
  userDiv.setAttribute("id", "user");
  userDiv.innerText = "User: " + text;
  conversation.appendChild(userDiv);
}

function addGptText(text) {
  //GPTの質問を表示する関数(questionGPT関数の中で使ってる)
  const gptDiv = document.createElement("div");
  gptDiv.setAttribute("id", "gpt");
  gptDiv.innerText = "GPT-3: " + text;
  conversation.appendChild(gptDiv);
}

function questionGpt(speech) {
  //gptが質問を作って表示してくれる関数
  fetch("/gpt", {
    method: "POST",
    body: new URLSearchParams({ speech }),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
    .then((response) => response.text())
    .then((gpt_response) => {
      addGptText(gpt_response);

      if ("speechSynthesis" in window) {
        const msg = new SpeechSynthesisUtterance();
        msg.text = gpt_response;
        msg.lang = "ja-JP";
        msg.rate = 0.9;
        msg.pitch = 1.2;
        speechSynthesis.speak(msg);
      }
    })
    .catch((e) => {
      console.error(e);
    });
}

function sendMessage(message) {
  addUserText(message); //ユーザの回答をdiv要素で追加

  if (endOnNextQuestion) {
    const username = document.body.dataset.username;

    fetch("/" + username + "/summary", {
      method: "POST",
      body: new URLSearchParams({
        prompt: message,
        date: document.querySelector("#date-form").value,
      }),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then(() => {
        window.location.href = "/" + username; // リダイレクト
        endOnNextQuestion = false; // リセット
      })
      .catch((error) => {
        console.error(error);
      });
  } else {
    questionGpt(message); //gptの回答をdiv要素で追加
  }
}

//ここから実行するJS

if (!localStorage.getItem("alerted")) {
  if ("speechSynthesis" in window) {
    alert("このブラウザは読み上げに対応しています。🎉");
  } else {
    alert("このブラウザは読み上げに対応していません。😭");
  }
  localStorage.setItem("alerted", "true");
}

function sendVoice() {
  //話しかけるボタンを押したら実行

  //radioButtonから言語を取得
  let voiceLang = document.querySelector(
    'input[name="voice-lang"]:checked'
  ).value;

  const recognition = new window.webkitSpeechRecognition();
  button.style.backgroundColor = "red"; //録音時のボタン色変える
  recognition.onresult = (event) => {
    const speech = event.results[0][0].transcript; //認識されたテキストを取得
    button.style.backgroundColor = ""; //ボタン色リセット

    sendMessage(speech);
  };

  //言語の設定
  switch (voiceLang) {
    case "japanese":
      recognition.lang = "ja-JP";
      break;
    default:
      recognition.lang = "en-US";
  }

  recognition.start();
}

function sendText() {
  //テキスト送信ボタンを押したら実行
  const inputText = document.getElementById("textInput").value;

  document.getElementById("textInput").value = ""; //テキストフィールドを空にする

  if (inputText === "") {
    alert("テキストを入力してください！");
  } else {
    sendMessage(inputText);
  }
}
