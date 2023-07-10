const button = document.querySelector("#button");
const conversation = document.querySelector("#conversation");

function addUserText(text) {
  const userDiv = document.createElement("div");
  userDiv.setAttribute("id", "user");
  userDiv.innerText = "User: " + text;
  conversation.appendChild(userDiv);
}

function addGptText(text) {
  const gptDiv = document.createElement("div");
  gptDiv.setAttribute("id", "gpt");
  gptDiv.innerText = "GPT-3: " + text;
  conversation.appendChild(gptDiv);
}

button.onclick = () => {
  //話しかけるボタンを押した時
  const recognition = new window.webkitSpeechRecognition();
  button.style.backgroundColor = "red"; //録音時のボタン色変える
  recognition.onresult = (event) => {
    const speech = event.results[0][0].transcript; //認識されたテキストを取得
    addUserText(speech); //音声入力テキストをdiv要素で追加
    button.style.backgroundColor = ""; //ボタン色リセット

    fetch("/gpt", {
      method: "POST",
      body: new URLSearchParams({ speech }),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
      .then((response) => response.text())
      .then((gpt_response) => {
        addGptText(gpt_response); //gptのレスポンスをdiv要素で追加
      })
      .catch((e) => {
        console.error(e);
      });
  };

  recognition.start();
};
