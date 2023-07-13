
let backgroundContainer = document.getElementsByClassName("background-container")[0];
let elementId = backgroundContainer.id;
let next_button = document.getElementById("next-button");
let back_button = document.getElementById("back-button");
let pen = document.getElementById("pen");
let kesigomu = document.getElementById("kesigomu");

// 前へボタンが押されたときの処理
back_button.addEventListener("click", function() {
  backgroundContainer.classList.add("next-rotate");
  pen.style.display = "none";
  kesigomu.style.display = "none";
  // アニメーション終了後
  backgroundContainer.addEventListener("animationend", function() {
  backgroundContainer.style.display = "none";
  backChangeContent(); 
  });
});

// 次へボタンが押されたときの処理
next_button.addEventListener("click", function() {
  backgroundContainer.classList.add("back-rotate");
  pen.style.display = "none";
  kesigomu.style.display = "none";
  // アニメーション終了後
  backgroundContainer.addEventListener("animationend", function() {
  backgroundContainer.style.display = "none";
  nextChangeContent();
  });
});

// 次へボタンを押されたときの表示日記の変更
function nextChangeContent() {
  let currentURL = window.location.href; // 現在のURLを取得
  let currentID = parseInt(elementId); // URLからpost_idを取得
  let newID = parseInt(currentID) + 1; // post_idを1加算
  let urlParts = currentURL.split("/"); // URLを"/"で分割した配列を取得
  urlParts[4] = newID; // 5番目の要素を置き換える
  let newURL = urlParts.join("/"); // 配列を"/"で結合して新しいURLを作成
  window.location.href = newURL; // 新しいURLに移動
}

// 前へボタンを押されたときの表示日記の変更
function backChangeContent() {
  let currentURL = window.location.href; // 現在のURLを取得
  let currentID = parseInt(elementId); // URLからpost_idを取得
  let newID = parseInt(currentID) - 1; // post_idを1減算
  let urlParts = currentURL.split("/"); // URLを"/"で分割した配列を取得
  urlParts[4] = newID; // 5番目の要素を置き換える
  let newURL = urlParts.join("/"); // 配列を"/"で結合して新しいURLを作成
  window.location.href = newURL; // 新しいURLに移動
}


