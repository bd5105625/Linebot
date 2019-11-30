import requests
# import numpy as np
import urllib3
from bs4 import BeautifulSoup

class ptt():
    def __init__(self , board):
        self.url = "https://www.ptt.cc/bbs/"
        board = board
        self.url = self.url + board + "/index.html"

    def get_all_href(self , url):
        payload = {
            # 'from' : url , 
            'yes' : 'yes'
        }
        # print(url)
        rs = requests.session()
        r = rs.post('https://www.ptt.cc/ask/over18' , verify = False , data=payload)
        r = rs.get(url , verify = False)        #此兩行為直接略過判定18歲的網址
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.select("div.nrec")
        # print(results)
        for item in results:
            num = item.text
            if num == "爆":
                self.article_push.append(100)
            elif num == '':
                self.article_push.append(0)
            elif num == 'X1' or num == 'X2' or num == 'X3' or num == 'X4' or num == 'X5' or num == 'X6' or num == 'X7' or num == 'X8' or num == 'X9' or num == 'XX':
                self.article_push.append(-1)
            elif num:
                self.article_push.append(int(num))
        # print(self.article_push)
        results = soup.select("div.title")
        for item in results:
            a_item = item.select_one("a")
            if a_item:  #確認該文章未被刪除
                href = 'https://www.ptt.cc'+ a_item.get('href')
                self.article_url.append(href)
            else:
                self.article_push.pop(len(self.article_url) - len(self.article_push))  #若該連結失效(文章被刪除) 把該文的推文數也pop
                
############################start here############################
    def run(self):
        # url = "https://www.ptt.cc/bbs/"
        # board = "Tainan"
        # url = url + board + "/index.html"
        self.article_url = []
        self.article_push = []   #推文數(包含爆)
        urllib3.disable_warnings()
        localurl = self.url
        for page in range(1,3):     #讀取除了首頁後的幾頁
            payload = {
                'from' : localurl , 
                'yes' : 'yes'
            }
            rs = requests.session()
            r = rs.post('https://www.ptt.cc/ask/over18' , verify = False , data=payload)
            r = rs.get(localurl , verify = False)
            soup = BeautifulSoup(r.text,"html.parser")
            btn = soup.select('div.btn-group > a')
            up_page_href = btn[3]['href']
            next_page_url = 'https://www.ptt.cc' + up_page_href
            localurl = next_page_url
            print(localurl)
            self.get_all_href(url = localurl)

        max = 0
        temp = []

        for i in range(0 , len(self.article_push)):
            temp.append(self.article_push[i])
        print(temp)
        self.article_push_list = []
        for i in range(0 , 5):  #二維list 共五組 每組第一個為推文數 第二個為index位子(即第幾篇文章的index)
            self.article_push_list.append([])    
        for j in range(0 , 5):
            max = 0
            for i in range(0 , len(self.article_push)):
                num = self.article_push[i]
                if num > max:
                    max = num
                    index = i
            self.article_push[index] = 0
            self.article_push_list[j].append(max)
            self.article_push_list[j].append(index)


        self.article_push = temp     #取回原本的push


        print(len(self.article_push))
        print(self.article_push_list)

        self.article_hot_url = []    #存取前幾熱門的文章網址
        for i in range(0 , 5):
            self.article_hot_url.append(self.article_url[self.article_push_list[i][1]])
            # print(self.article_url[self.article_push_list[i][1]])