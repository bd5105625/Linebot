from transitions.extensions import GraphMachine

from utils import send_text_message
from ptt import ptt
from hotarticle import hotarticle

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event , string):
        text = event.message.text
        return text.lower() == "熱門文章"

    def is_going_to_state2(self, event , string):
        text = event.message.text
        return text.lower() == "熱門新聞"

    def is_going_to_state3(self, event , string):
        text = event.message.text
        return text.lower() == "看板功能"

    def is_going_to_state4(self, event , string):
        text = event.message.text
        return text.lower() == "最新文章"
 
    def is_going_to_state5(self, event , string):
        text = event.message.text
        return text.lower() == "看板最新文章"   #所選看板的最新文章

    def is_going_to_state6(self, event , string):
        text = event.message.text
        return text.lower() == "看板熱門文章"   #所選看板的熱門文章

    def on_enter_state1(self, event , string):
        print("I'm entering state1" , string) 
        # self.gethot(event)

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event , string):
        print("I'm entering state2" , string)
        # self.getnews(event)

    def on_exit_state2(self):
        print("Leaving state2")

    # def on_enter_state3(self, event , string):
    #     print("I'm entering state3" , string)

    # def on_exit_state3(self):
    #     print("Leaving state3")

    def on_enter_state4(self, event , string):
        print("I'm entering state4" , string)
        # self.getarticle(event)

    def on_exit_state4(self):
        print("Leaving state4")

    def on_enter_state5(self, event , string):
        print("I'm entering state5" , string)
        # self.getarticle(event)

    def on_exit_state5(self):
        print("Leaving state5")

    def on_enter_state6(self, event , string):
        print("I'm entering state6" , string)
        # self.getarticle(event)

    def on_exit_state6(self):
        print("Leaving state6")

    def getboard(self , event , string):    #從特定看板取得前五熱門文章
        reply_token = event.reply_token
        run = ptt(string)
        run.run()
        string = ""
        if run.article_hot_url != []:
            for i in range(0 , 8):
                string = string + run.article_hot_title[i] + "\n" + run.article_hot_url[i] + "\n"
        else:
            string = "錯誤看板名稱，請重新點選\"選擇看板\""
        send_text_message(reply_token , string)
        print("back to user")
        self.go_back()

    def gethot(self , event):      #取得熱門文章
        reply_token = event.reply_token
        run = hotarticle()
        run.runhot()
        string1 = ""
        # string2 = ""
        for i in range(0 , 10):
            string1 = string1 + run.hotarticle_title[i] + "\n" + run.hotarticle_url[i] + "\n"
        # for i in range(5 , 10):
        #     string2 = string2 + run.hotarticle_url[i] + "\n\n"
        send_text_message(reply_token , string1)
        # send_text_message(reply_token , string2)
        print("back to user")        
        self.go_back()

    def getnews(self , event):      #取得熱門新聞
        reply_token = event.reply_token
        run = hotarticle()
        run.runnews()
        string = ""
        for i in range(0 , 10):
            string = string + run.hotarticle_title[i] + "\n" + run.newsarticle_url[i] + "\n"
        send_text_message(reply_token , string)
        print("back to user")        
        self.go_back()

    def getarticle(self , event):      #取得最新文章
        reply_token = event.reply_token
        run = hotarticle()
        run.newarticle()
        string = ""
        for i in range(0 , 10):
            string = string + run.hotarticle_title[i] + "\n" + run.article_url[i] + "\n"
        send_text_message(reply_token , string)
        print("back to user")        
        self.go_back()

    def getboardnew(self , event , string):
        reply_token = event.reply_token
        run = ptt(string)
        run.boardnewarticle()
        if run.boardurl != []:
            for i in range(0 , len(run.boardurl)):
                string = string + run.boardtitle[i] + "\n" + run.boardurl[i] + "\n"
        send_text_message(reply_token , string)
        print("back to user")
        self.go_back()    

