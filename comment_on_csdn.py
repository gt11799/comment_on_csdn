#!/usr/bin/env python
# _*_coding=utf8 _*_
'''
login csdn and comment on the article(mine :D)
'''

import requests
import cookielib
import random
import time
from lxml import etree

class CsdnSpider(object):
    
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.url = 'https://passport.csdn.net/account/login'
        
        self.jar = cookielib.CookieJar()
        self.pwd = {
            'username':self.login,
            'password':self.password,
            '_eventId':'submit',
        }
        self.header = {
            'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',
            '(Request-Line)':'POST /account/login?ref=toolbar HTTP/1.1',
            'Host':'passport.csdn.net',
            'Referer':'https://passport.csdn.net/account/login?ref=toolbar',
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        self.header['Content-Length'] = '129'
        #if change the account or password, it will change.
        
    def login_csdn(self):
        self.session = requests.session()
        self.response = self.session.get(self.url, cookies=self.jar)
        print("Geted request...")
        self.parse = etree.HTML(self.response.text)
        self.webflow = self.parse.xpath('//input[@name="lt"]/@value')
        self.execution = self.parse.xpath('//input[@name="execution"]/@value')
        #print self.webflow[0], self.execution[0]
        self.pwd["lt"] = self.webflow[0]
        self.pwd["execution"] = self.execution[0]
        print self.pwd
        
        self.response = self.session.post(self.url, headers=self.header, data=self.pwd)
        print("Posted pwd....")
        #import pdb; pdb.set_trace()
               
    def post_comment(self, article, comment):
       '''
       comment on the article, article is the code of article
       need login first.
       ''' 
       self.post_header = {
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',
           '(Request-Line)':'POST /gt11799/comment/submit?id=39560737 HTTP/1.1',
           'Host':'blog.csdn.net',
           'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
           'Accept-Encoding':'gzip, deflate',
           'Connetction':'keep-alive',
           'Accept':'*/*',
           'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With':'XMLHttpRequest',
           'Pragma':'no-cache',
           'Cache-Control':'no-cache',
       }
       
       print("article: %s, comment: %s" %(article, comment))
       
       #get the request_line, post_url and article_url
       request_line = 'POST /gt11799/comment/submit?id=' + article + ' HTTP/1.1'
       referer = 'http://blog.csdn.net/gt11799/article/details/' + article
       post_url = 'http://blog.csdn.net/gt11799/comment/submit?id=' + article
       
       self.post_header['(Request-Line)'] = request_line
       self.post_header['Referer'] = referer
       
       post_data = {
           'commentid':None,
           'content':comment,
           'replyld':None,
       }
       
       #get the Content_Length
       content_length = str(28 + 3 * len(comment))
       self.post_header['Content-Length'] = content_length
       print self.post_header
       
       self.response = self.session.post(post_url, headers=self.post_header, data = post_data)
       print("Have commented, please check.....")        
       
       #import pdb; pdb.set_trace()
           
        
if __name__ == '__main__':
    article_list = ['39255873', '39560737', '39553767', '39552299', '39505093', '39482877', '39349359', '39453857']
    comment_list = [
        '楼主讲解的不太明白哎',
        '楼主好棒，继续加油',
        '我去，我也可以当水军了',
        '这都是我自己刷的评论，不必理会',
        '话说我是有多无聊',
    ]
    spider = CsdnSpider('user', 'password')
    spider.login_csdn()
    while True:
        article = random.choice(article_list)
        comment = random.choice(comment_list)
        spider.post_comment(article, comment)
        time.sleep(600)
