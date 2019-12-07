# import requests
# from bs4 import BeautifulSoup
# url="https://www.ptt.cc/bbs/gossiping/index.html"

# def get_all_href(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, "html.parser")
#     results = soup.select("div.title")
#     for item in results:
#         a_item = item.select_one("a")
#         title = item.text
#         if a_item:
#             print(title, 'https://www.ptt.cc'+ a_item.get('href'))
        
# for page in range(1,2):
#     payload = {
#         'from' : url , 
#         'yes' : 'yes'
#     }
#     rs = requests.session()
#     r = rs.post('https://www.ptt.cc/ask/over18' , verify = False , data=payload)
#     r = rs.get(url , verify=False)
#     soup = BeautifulSoup(r.text,"html.parser")
#     for entry in soup.select('.r-ent'):
#         print (entry.select('.date')[0].text , entry.select('.author')[0].text , entry.select('.title')[0].text)
#     # print(soup)
#     # btn = soup.select('div.btn-group > a')
#     # up_page_href = btn[3]['href']
#     # next_page_url = 'https://www.ptt.cc' + up_page_href
#     # url = next_page_url
#     # get_all_href(url = url)

# num = "asd"
# print(type(num))
# a = True
# if a:
#     print("123")
# if type(num) == str:
#     print("right")
#     a = False
# if a:
#     print("123")
# abc = [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8]
# abc.pop(6-(len(abc)))
# print(abc)
# from ptt import *
# run()

from ptt import *
signal = ""
run = ptt("gossiping")
run.run()
string = ""
if run.article_hot_url != []:
    for i in range(0 , 5):
        # print(run.article_hot_url[i])
        string = string + run.article_hot_title[i] + "\n" + run.article_hot_url[i] + "\n"
else:
    print("Error")
print("\n" , string)
# from hotarticle import *
# run = hotarticle()
# run.newarticle()
# # run.runnews