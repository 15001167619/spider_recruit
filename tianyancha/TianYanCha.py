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


# 公司存储excel
JOB_EXCEL_PATH = 'G:\\tianyancha\\job.xlsx'

spider_company_headers = {

}

class TianYanCha:

    def __init__(self):
        """ 公司官网地址 """
        self.index_url = 'https://www.tianyancha.com/'
        """ 地区代码列表 """
        self.tyc_area_api = "https://xcx.qichacha.com/wxa/v1/admin/getAreaList"
        """ 地区代码列表 """
        self.tyc_search_url = "https://www.tianyancha.com/search/pPageNum?base=area_code"
        """ 地区代码列表 """
        self.tyc_search_url = "https://www.tianyancha.com/contact/sendCard/3330338714.json"
        """ headers """
        self.header = {'User-Agent': random.choice(headers)}

        self.spider_company_headers = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'ssuid=5285871275; TYCID=636019c0d45211e985baefd6bd263e3b; undefined=636019c0d45211e985baefd6bd263e3b; _ga=GA1.2.1545809170.1568178593; _gid=GA1.2.1037819465.1568178593; RTYCID=4bc586956a054943a824982b367128e7; CT_TYCID=8ed16940a52b4498afdc8f929d88018d; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25221%2522%252C%2522contactNumber%2522%253A%252213811491190%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%252286%2525%2522%252C%2522state%2522%253A%25225%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522surday%2522%253A%2522179%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252298%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25226%2522%252C%2522claimUnread%2522%253A%25222%2522%252C%2522claimPoint%2522%253A%25221%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzgxMTQ5MTE5MCIsImlhdCI6MTU2ODI1NDQ0NywiZXhwIjoxNTk5NzkwNDQ3fQ.gjFMkM6R8yB3j_EbQSvx2CHI7mcDDeI00kd1XZVPS7Rw0jDZYoy5JCWkPIoPXhi_egg-MOJn1JViWAr9bqlmuQ%2522%252C%2522vipToTime%2522%253A%25221583670010592%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522industry%2522%253A%2522IT%257C%25E9%2580%259A%25E4%25BF%25A1%257C%25E7%2594%25B5%25E5%25AD%2590%257C%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522post%2522%253A%2522IT%257C%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%257C%25E9%2580%259A%25E4%25BF%25A1%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522claimDetailLevel%2522%253A%252218%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%2597%25B6%25E4%25BB%25A3%25E5%2588%259B%25E4%25BF%25A1%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25222%2522%252C%2522companyName%2522%253A%2522%25E5%258C%2597%25E4%25BA%25AC%25E6%2597%25B6%25E4%25BB%25A3%25E5%2588%259B%25E4%25BF%25A1%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522realName%2522%253A%2522%25E9%25A9%25AC%25E6%25B4%25AA%25E5%25AE%2587%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252220%2522%252C%2522mobile%2522%253A%252213811491190%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzgxMTQ5MTE5MCIsImlhdCI6MTU2ODI1NDQ0NywiZXhwIjoxNTk5NzkwNDQ3fQ.gjFMkM6R8yB3j_EbQSvx2CHI7mcDDeI00kd1XZVPS7Rw0jDZYoy5JCWkPIoPXhi_egg-MOJn1JViWAr9bqlmuQ; aliyungf_tc=AQAAAP80ZxyezwwA6cExPUG3Qh+vZD8K; bannerFlag=undefined; csrfToken=ifMcYo5TwwbAhppZqdQWubZ9; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568179059,1568189249,1568254383,1568264255; cloud_token=fceeba0776ef4ccaaaff8308e9b4f37f; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568274868',
                'Host': 'www.tianyancha.com',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    def spider_company(self, area_list):
        #print(area_list)
        for area_code in area_list:
            print("地区编号：" + area_code)
            search_url = self.tyc_search_url.replace("PageNum","1").replace("area_code",area_code)
            print(search_url)
            res = requests.get(search_url, headers=self.spider_company_headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            # 打印结构化数据
            #print(soup.prettify())
            total_page_num = soup.find('input', id='pg_customize_total')["value"]
            search_url = search_url.replace("1","PageNum")
            self.get_company_list(search_url,total_page_num)


    def spider(self):
        # 抓取首页地址
        print('公司详情页' + self.index_url)
        res = requests.get(self.tyc_area_api, headers=self.header)
        soup = BeautifulSoup(res.text, 'html.parser')
        area_data = json.loads(str(soup))
        # 打印结构化数据
        #print(area_data['result'])
        area_list = []

        for area_info in area_data['result']:
            #print(area_info)
            area_code = area_info['code']
            if area_code != '':
                area_list.append(str(area_code).lower())

        self.spider_company(area_list)

    def get_company_list(self, search_url, total_page_num):

        for page_num in range(int(total_page_num)):
            page_num = page_num + 1
            search_url = search_url.replace("PageNum",str(page_num))
            print(search_url)
            res = requests.get(search_url, headers=self.spider_company_headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            # 打印结构化数据
            #print(soup.prettify())

            print(soup.find_all("div",class_='content'))
            search_url = search_url.replace(str(page_num),"PageNum")




if __name__ == '__main__':

    tianyancha = TianYanCha()
    tianyancha.spider()