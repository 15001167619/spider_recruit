import requests
# 导入文件操作库
import os
import time
import json
import random
import pandas as pd
from bs4 import BeautifulSoup

headers = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        ]





class Movie:

    def __init__(self):
        # 少年的你
        self.index_url = 'https://movie.douban.com/subject/30166972/comments?status=P'

        self.next_url = 'https://movie.douban.com/subject/30166972/comments?start=20&limit=20&sort=new_score&status=P'
        # boss直聘城市地址
        self.city_url = 'https://movie.douban.com/subject/30166972/comments?start=40&limit=20&sort=new_score&status=P'
        # boss直聘职位地址
        self.jobs_url = 'https://m.zhipin.com/wapi/zpgeek/mobile/jobs.json'
        # 请求头 headers
        self.header = {'User-Agent': random.choice(headers)}
        # 请求间隔时长 interval_time
        self.interval_time = 20

    def getOnePageComment(id, pageNum):
        # 根据页数确定start变量的值
        start = (pageNum - 1) * 20
        url = "https://movie.douban.com/subject/%s/comments?start=" \
              "%s&limit=20&sort=new_score&status=P" % (id, start)
        # 爬取评论信息的网页内容
        content = requests.get(url).text
        # 通过bs4分析网页
        soup = BeautifulSoup(content, 'html5lib')
        # 分析网页得知， 所有的评论信息都是在span标签， 并且class为short;
        commentsList = soup.find_all('span', class_='short')
        pageComments = ""
        ## 依次遍历每一个span标签， 获取标签里面的评论信息, 并将所有的评论信息存储到pageComments变量中;
        for commentTag in commentsList:
            pageComments += commentTag.text
        print("%s page" % (pageNum))
        global comments
        comments += pageComments





    def spider(self):
        """
        获取 少年的你 短评
        :return:
        """
        r = requests.get(self.index_url, headers=self.header, timeout=self.interval_time)
        soup = BeautifulSoup(r.text, 'html.parser')
        commentsList = soup.find_all('div', class_='comment-item')




        for commentsInfo in commentsList:
            print('##############################################')
            print('##############################################')
            print('##############################################')
            avatar_div = commentsInfo.find_all('div', class_='avatar')
            comment_div = commentsInfo.find_all('div', class_='comment')
            print('##############################################')
            # 评论人主页地址
            userSiteUrl = avatar_div[0].find('a').get('href')
            print('【评论人主页地址】:' + userSiteUrl)
            userName = avatar_div[0].find('a').get('title')
            print('【评论人昵称】:' + userName)
            # 评论人头像
            userHeadPic = commentsInfo.find_all('img')[0].get('src')
            print('【评论人头像】:' + userHeadPic)
            # 有用数
            commentVote = comment_div[0].find_all('span', class_='votes')[0].text
            print('【有用数】:' + commentVote)
            # 评论时间
            commentTime = comment_div[0].find_all('span', class_='comment-time')[0].get('title')
            print('【评论时间】:' + commentTime)
            # 评论内容
            shortComment = comment_div[0].find_all('span', class_='short')[0].text
            print('【评论内容】:' + shortComment)




if __name__ == '__main__':
    movie = Movie()
    movie.spider()
