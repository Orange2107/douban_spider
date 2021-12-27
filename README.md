# douban_spider. A easy program to practice spider skill
**使用Python使用对豆瓣电影top250进行爬虫**
- getdata函数
  - askurl函数
    - 使用urllib.request.Request，封装浏览器信息成为一个对象（req)，目的是把Python伪装成浏览器。
    - 使用urllib.request.openurl，把对象req发送给服务器，获得服务器返回数据。
  - 使用Beautifusoup对返回的数据进行解析，采用fin_all函数查找带有目的数据的模块。
  - 使用正则表达式对模块中信息进行提取
- savedata函数
  - 存入excel表格或者放入数据库中
![image](https://user-images.githubusercontent.com/70784569/147428914-f80c5b77-2706-468e-9a0c-dc758d8f9ed2.png)
