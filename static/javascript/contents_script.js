let next_button = document.getElementById("next-button");
let back_button = document.getElementById("back-button");
let pen = document.getElementById("pen");
let kesigomu = document.getElementById("kesigomu");
let nowContainer = document.getElementsByClassName("now")[0];//現在のページ
let pastContainer = document.getElementsByClassName("past")[0];//前のページ
let pastid = pastContainer.id; //前のid
let nextContainer = document.getElementsByClassName("next")[0];//次のページ
let nextid = nextContainer.id; //次のid
let change = document.getElementsByClassName("change")[0]; 

// 前へボタンが押されたときの処理
back_button.addEventListener("click", function() {
  nowContainer.classList.add("back-rotate");
  pastContainer.style.display = "block" //前のページを表示
  pen.style.display = "none";
  kesigomu.style.display = "none"; 
  change.style.display = "none";
  // アニメーション終了後
  nowContainer.addEventListener("animationend", function() {
  nowContainer.style.display = "none";
  pastContainer.style.display = "none"
  backChangeContent(); 
  });
});

// 次へボタンが押されたときの処理
next_button.addEventListener("click", function() {
  nowContainer.classList.add("next-rotate");
  nextContainer.style.display = "block" //次のページを表示
  pen.style.display = "none";
  kesigomu.style.display = "none";
  change.style.display = "none";
  console.log(nextid);
  // アニメーション終了後
  nowContainer.addEventListener("animationend", function() {
  nowContainer.style.display = "none";
  nextContainer.style.display = "none"
  nextChangeContent();
  });
});


// 前へボタンが押されたときの表示日記の変更
function backChangeContent() {
  let currentURL = window.location.href; // 現在のURLを取得
  let newID = pastid; // 前のidを取得
  let urlParts = currentURL.split("/"); // URLを"/"で分割した配列を取得
  urlParts[4] = newID; // 5番目の要素を置き換える
  let newURL = urlParts.join("/"); // 配列を"/"で結合して新しいURLを作成
  window.location.href = newURL; // 新しいURLに移動
}

// 次へボタンが押されたときの表示日記の変更
function nextChangeContent() {
  let currentURL = window.location.href; // 現在のURLを取得
  let newID = nextid; // 次のidを取得
  let urlParts = currentURL.split("/"); // URLを"/"で分割した配列を取得
  urlParts[4] = newID; // 5番目の要素を置き換える
  let newURL = urlParts.join("/"); // 配列を"/"で結合して新しいURLを作成
  window.location.href = newURL; // 新しいURLに移動
}

