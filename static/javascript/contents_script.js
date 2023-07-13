// 次へボタンが押されたときの処理
var backgroundContainer = document.getElementsByClassName("background-container")[0];
var elementId = backgroundContainer.id;
var next_button = document.getElementById("next-button");
var back_button = document.getElementById("back-button");

back_button.addEventListener("click", function() {
  backgroundContainer.classList.add("next-rotate");
  backgroundContainer.addEventListener("animationend", function() {
  backgroundContainer.style.display = "none";
  // var myElement = document.getElementById("myElement");
  // myElement.textContent = elementId;
  backChangeContent();
    
  });
});

// 前へボタンが押されたときの処理

next_button.addEventListener("click", function() {
  backgroundContainer.classList.add("back-rotate");
  backgroundContainer.addEventListener("animationend", function() {
  backgroundContainer.style.display = "none";
  nextChangeContent();
  });
});

// 次へボタンを押されたときの表示日記の変更
function nextChangeContent() {
  var currentURL = window.location.href; // 現在のURLを取得
  var currentID = parseInt(elementId); // URLからIDを取得
  var newID = parseInt(currentID) + 1; // IDを1加算
  var urlParts = currentURL.split("/"); // URLを"/"で分割した配列を取得
  urlParts[4] = newID; // 5番目の要素を置き換える
  var newURL = urlParts.join("/"); // 配列を"/"で結合して新しいURLを作成
  window.location.href = newURL; // 新しいURLに移動
}

// 前へボタンを押されたときの表示日記の変更
function backChangeContent() {
  var currentURL = window.location.href; // 現在のURLを取得
  var currentID = parseInt(elementId); // URLからIDを取得
  var newID = parseInt(currentID) - 1; // IDを1加算
  var urlParts = currentURL.split("/"); // URLを"/"で分割した配列を取得
  urlParts[4] = newID; // 5番目の要素を置き換える
  var newURL = urlParts.join("/"); // 配列を"/"で結合して新しいURLを作成
  window.location.href = newURL; // 新しいURLに移動
}


