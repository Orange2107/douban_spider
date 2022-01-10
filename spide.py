# -*- coding = utf-8 -*-
# @Time : 2021/12/21 8:41 PM
# @Author : CZJ
# @File  :   spide.py
# @software : PyCharm

import re     #正则表达式，进行文字匹配
from bs4 import BeautifulSoup  #网页解析，获取数据
import urllib.request, urllib.error #制定url，获取页面
import xlwt  #进行excel操作
import sqlite3 #进行sql数据库操作

#获取数据
def getData(baseurl):
    datalist = []
    images = []
    names = []
    score = []
    words = []
    person = []
    actor = []
    for i in range(0, 10):
        url = baseurl + str(i*25)
        html = askUrl(url)    #获取一个页面的html代码
        #逐一解析
        page = BeautifulSoup(html, "html.parser")  #创建解析后的对象
        movies = page.find_all('div', class_="item")  #作用是查找模块，需要保证每个模块结构都一致，形成25个。
        for item in movies:
            #正则匹配，找到图片的地址
            datas = []  # 存放每一部电影的数据
            item = str(item)
            names = re.findall(link_name, item)  # 加上零就是该数组里的值

            if len(names) >= 2:    #对多个名称的处理
                datas.append(names[0])  #中文名称
                outname = names[1]     #取出来后变成了str
                outname = outname.replace("/","")
                outname = outname.replace("\xa0", "")
                datas.append(outname)  #外文名字
            else:
                datas.append(names[0])
                datas.append("NO RESULT")  #留空
            details = re.findall(link_detail, item)[0]
            datas.append(details)
            images = re.findall(link_img, item)[0]
            datas.append(images)

            #评分
            score = re.findall(link_score, item)[0]
            datas.append(score)
            #经典台词
            words = re.findall(link_words, item)
            if len(words) > 0:
                words = words[0].replace("'","")  #去掉句号
                datas.append(words)
            else:
                datas.append("NO RESULT")       #当数据不存在时，需要加入空格占位
            person = re.findall(link_person, item)[0]
            datas.append(person)
            #演员
            actor = re.findall(link_actor, item)[0]  #找到的类型是list
            actor = actor.replace("\n", "")
            actor = actor.replace("<br/>", "")
            actor = actor.replace("\xa0", "")
            actor = actor.strip()       #去掉前后的空格
            datas.append(actor)
            datalist.append(datas)
    return  datalist







#得到一个指定URL的网页内容
def askUrl(url):
    head = {

        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }   #告诉豆瓣服务器，我们是什么类型的浏览器
    req = urllib.request.Request(url=url, headers=head)  #构造一个对象，封装浏览器信息
    html = ""   #字符串
    try:
        response = urllib.request.urlopen(req)  #构造http请求，发生给服务器   urllib.request可以用来发送request和获取request的结果
        html = response.read().decode('utf-8')  #接受数据，并且进行编码
    except Exception as aresult:
        print(aresult)
    return html



#保存在excel中
#def saveData(datalist, savepath):
    # workbook = xlwt.Workbook(encoding='utf-8')
    # my_sheet = workbook.add_sheet("top_films", cell_overwrite_ok=True)
    # col = ('电影名称', '外文名称', '详情网站', '图片地址', '评分', '经典台词', '评价人数', '演员与类型')
    # for i in range(0, 8):
    #     my_sheet.write(0, i, col[i]) #书写头行
    # for count in range(0, 250):
    #     temp = datalist[count]
    #     for head in range(0, 8):
    #         my_sheet.write(count+1, head, temp[head])
    # workbook.save(savepath)


def saveDB(datalist, dbpath):
    initdb(dbpath)
    db = sqlite3.connect(dbpath)
    flag = db.cursor()
    for movie in datalist:   #把每行进行处理
        count = -1
        info = ""
        for col in movie:   #对每一列进行解析  046
            count+=1
            if count == 4:
                info = info + ","+col  #是数字或者自带引号的
                continue
            if count == 0:
                info = '"' + str(col) + '"'
                continue
            col = '"' + str(col) + '"'  # 加上上标作为字符串输入
            info = info + ","+col
        print(info)
        sql = '''
            insert into movie(
            name, foreign_name, detail, image, score, sentence, number, actors)
            values (%s) '''% info     #把每一列合并
        flag.execute(sql)
        print("插入成功")
    db.commit()
    db.close()



def initdb(dbpath):
    db = sqlite3.connect(dbpath)
    flag = db.cursor()
    print("数据库创建成功")
    sql = '''
        create table movie(
        id integer primary key autoincrement,
        name text not null,
        foreign_name text not null,
        detail text not null,
        image text not null,
        score real not null,
        sentence text  not null,
        number text not null,
        actors text not null
        )
    '''
    flag.execute(sql)
    db.commit()
    db.close()







if __name__ == "__main__":   #当程序执行时干的事
    baseurl = "https://movie.douban.com/top250?start="
    datalist = []  # 存放总共电影
    link_detail = re.compile((r'<a href="(.*?)">'))
    link_img = re.compile(r'<img .* src="(.*?)" width="100"/>',re.S)   #影片的图片
    link_name = re.compile(r'<span class="title">(.*?)</span>')
    link_score = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
    link_words = re.compile(r'<span class="inq">(.*?)</span>')
    link_person = re.compile(r'<span>(\d*?.*?)</span>')
    link_actor = re.compile(r'<p class="">(.*?)</p>',re.S)
    #爬取数据movie
    datalist = getData(baseurl)
    #保存数据,使用excel
    #savepath = "豆瓣电影top250.xls"
    #saveData(datalist, savepath)
    #保存数据，使用sqlite
    dbpath = "movie250.db"
    saveDB(datalist, dbpath)