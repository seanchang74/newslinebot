# NewsLinebot 新聞爬取機器人
**使用NEWS API作為資料蒐集來源，透過圖文選單，選擇不同的資料獲取方式**
## 加入好友(二擇一即可)
1. 開啟LINE搜尋ID"@827hoihe"加入好友
2. 直接點選下方連結，加入好友<br>
<a href="https://lin.ee/DdyHHHB"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/zh-Hant.png" alt="加入好友" height="36" border="0"></a>
## 圖文選單選項
1. 隨便看看
  * 新聞來源 : ettoday.net, setn.com, ltn.com.tw, udn.com, bbc.com, cw.com.tw
  * 使用datetime.today()，因此只顯示本日新聞
  * 使用newsapi.get_everything方法
2. 今日頭條
  * 先使用QuickReply篩選頭條新聞類別
  * 使用newsapi.get_top_headlines方法
3. 關鍵字搜索
  * 結合PostgreSQL儲存使用者欲搜尋的內容
  * 使用newsapi.get_everything方法
4. 聯絡我們
  * 使用liff-v2設計回饋表單
  * 將使用者送出的表單資料儲存在PostgreSQL中
