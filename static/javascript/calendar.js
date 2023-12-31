const week = ["日", "月", "火", "水", "木", "金", "土"];
const today = new Date();
// 月末だとずれる可能性があるため、1日固定で取得
var showDate = new Date(today.getFullYear(), today.getMonth(), 1);

// 初期表示
window.onload = function () {
  showProcess(today, calendar);
};
// 前の月表示
function prev() {
  showDate.setMonth(showDate.getMonth() - 1);
  showProcess(showDate);
}

// 次の月表示
function next() {
  showDate.setMonth(showDate.getMonth() + 1);
  showProcess(showDate);
}

// カレンダー表示
function showProcess(date) {
  var year = date.getFullYear();
  var month = date.getMonth();

  document.querySelector(".subtitle").innerHTML = month + 1 + "月のちょこっと";
  document.querySelector("#header").innerHTML =
    year + "年 " + (month + 1) + "月";

  const processPromise = createProcess(year, month);
  processPromise.then((process) => {
    document.querySelector("#calendar").innerHTML = process;
  });
}

// カレンダー作成
function createProcess(year, month) {
  // 曜日
  var calendar = "<table><tr class='dayOfWeek'>";
  for (var i = 0; i < week.length; i++) {
    calendar += "<th>" + week[i] + "</th>";
  }
  calendar += "</tr>";

  var count = 0;
  var startDayOfWeek = new Date(year, month, 1).getDay();
  var endDate = new Date(year, month + 1, 0).getDate();
  var lastMonthEndDate = new Date(year, month, 0).getDate();
  var row = Math.ceil((startDayOfWeek + endDate) / week.length);

  const username = document.body.dataset.username;

  //データ要求
  const diaryDataPromise = requestDiaryData(year, month + 1, username);
  return diaryDataPromise.then((diaryData) => {
    //diaryDataは、date,post_id,titleのオブジェクトの配列であるjson

    // 1行ずつ設定
    for (var i = 0; i < row; i++) {
      calendar += "<tr>";
      // 1colum単位で設定
      for (var j = 0; j < week.length; j++) {
        if (i == 0 && j < startDayOfWeek) {
          // 1行目で1日まで先月の日付を設定
          calendar +=
            "<td class='disabled'>" +
            (lastMonthEndDate - startDayOfWeek + j + 1) +
            "</td>";
        } else if (count >= endDate) {
          // 最終行で最終日以降、翌月の日付を設定
          count++;
          calendar += "<td class='disabled'>" + (count - endDate) + "</td>";
        } else {
          // 当月の日付を曜日に照らし合わせて設定
          count++;

          //日記がある場合、contentRefにそのhtmlのa要素を取得
          let contentRef = "";
          if (
            (obj = diaryData.find((item) => {
              return item.date === count;
            }))
          ) {
            contentRef = `<a href='/${username}/${obj.post_id}/contents' class='cell-title'>${obj.title}</a>`;
          }

          if (
            year == today.getFullYear() &&
            month == today.getMonth() &&
            count == today.getDate()
          ) {
            calendar += "<td class='today'>" + count + contentRef + "</td>";
            // pin画像追加
            // calendar += `<td class='today'>
            // <img class='pin' src='/static/css/img/pngegg.png'>
            // ${count}
            // ${contentRef}
            // </td>`;
          } else {
            calendar += `<td><div class='cell-content'>${count}${contentRef}</div></td>`;
          }
        }
      }
      calendar += "</tr>";
    }
    return calendar;
  });
}

//データ要求
function requestDiaryData(year, month, username) {
  data = {
    year: year,
    month: month,
    username: username,
  };

  // promiseオブジェクトを返す
  return fetch("/cal", {
    method: "POST",
    headers: { "Content-Type": "application/json" }, //
    body: JSON.stringify(data), //もっとやりようありそうだけどとりあえずこの形で
  })
    .then((response) => response.json())
    .then((date) => {
      //変数名が不適切?
      const result = date.result;
      return result;
    })
    .catch((error) => {
      console.error(error);
    });
}
