// JavaScript
// ページの読み込みが完了したら処理を開始する

$('.slider').slick({
  autoplay: true,//自動的に動き出すか。初期値はfalse。
  infinite: true,//スライドをループさせるかどうか。初期値はtrue。
  slidesToShow: 5,//スライドを画面に3枚見せる
  slidesToScroll: 5,//1回のスクロールで3枚の写真を移動して見せる
  prevArrow: '<div class="slick-prev"></div>',//矢印部分PreviewのHTMLを変更
  nextArrow: '<div class="slick-next"></div>',//矢印部分NextのHTMLを変更
  dots: true,//下部ドットナビゲーションの表示
  responsive: [
    {
      breakpoint: 3300,//モニターの横幅が3300px以下の見せ方
      settings: {
        slidesToShow: 4,//スライドを画面に2枚見せる
        slidesToScroll: 4,//1回のスクロールで2枚の写真を移動して見せる
      }
    },
    {
      breakpoint: 2600,//モニターの横幅が2600px以下の見せ方
      settings: {
        slidesToShow: 3,//スライドを画面に2枚見せる
        slidesToScroll: 3,//1回のスクロールで2枚の写真を移動して見せる
      }
    },
    {
    breakpoint: 769,//モニターの横幅が769px以下の見せ方
    settings: {
      slidesToShow: 2,//スライドを画面に2枚見せる
      slidesToScroll: 2,//1回のスクロールで2枚の写真を移動して見せる
    }
  },
  {
    breakpoint: 426,//モニターの横幅が426px以下の見せ方
    settings: {
      slidesToShow: 1,//スライドを画面に1枚見せる
      slidesToScroll: 1,//1回のスクロールで1枚の写真を移動して見せる
    }
  }
]
});
