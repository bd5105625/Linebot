import requests
import urllib3
from bs4 import BeautifulSoup

class hotarticle():
    def __init__(self):
        self.hoturl = "https://pttweb.tw/hot-threads"
        self.newsurl = "https://pttweb.tw/news"
        self.newarticleurl = "https://pttweb.tw/newest-threads"
        self.hotarticle_title = []

    def runhot(self):
        self.hotarticle_url = []
        urllib3.disable_warnings()
        r = requests.get(self.hoturl , verify=False)
        soup = BeautifulSoup(r.text , "html.parser")
        results = soup.select("div.thread-item")
        for item in results:
            a_item = item.select_one("a")
            if a_item:
                href = 'https://pttweb.tw' + a_item.get('href')
                self.hotarticle_url.append(href)
                self.hotarticle_title.append(a_item.text)
        string = ""
        for i in range(0 , len(self.hotarticle_url)):
            string = string + "\n" + self.hotarticle_url[i]
        print(string)
    
    def runnews(self):
        self.newsarticle_url = []
        urllib3.disable_warnings()
        r = requests.get(self.newsurl , verify=False)
        soup = BeautifulSoup(r.text , "html.parser")
        results = soup.select("div.thread-item")
        for item in results:
            a_item = item.select_one("a")
            if a_item:
                href = 'https://pttweb.tw' + a_item.get('href')
                self.newsarticle_url.append(href)
                self.hotarticle_title.append(a_item.text)
        string = ""
        for i in range(0 , len(self.newsarticle_url)):
            string = string + "\n" + self.newsarticle_url[i]
        print(string)

    def newarticle(self):
        self.article_url = []
        urllib3.disable_warnings()
        r = requests.get(self.newarticleurl , verify=False)
        soup = BeautifulSoup(r.text , "html.parser")
        results = soup.select("div.thread-item")
        for item in results:
            a_item = item.select_one("a")
            if a_item:
                href = 'https://pttweb.tw' + a_item.get('href')
                self.article_url.append(href)
                self.hotarticle_title.append(a_item.text)
        string = ""
        for i in range(0 , len(self.article_url)):
            string = string + "\n" + self.article_url[i]
        print(string)
        print(len(self.article_url))