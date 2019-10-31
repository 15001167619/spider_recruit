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


# 职位存储excel
JOB_EXCEL_PATH = 'G:\\boss_zhipin\\job.xlsx'


class SpiderBossZhiPin:

    def __init__(self):
        # boss直聘首页
        self.index_url = 'https://m.zhipin.com'
        # boss直聘城市地址
        self.city_url = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
        # boss直聘职位地址
        self.jobs_url = 'https://m.zhipin.com/wapi/zpgeek/mobile/jobs.json'
        # 请求头 headers
        self.header = {'User-Agent': random.choice(headers)}
        # 请求间隔时长 interval_time
        self.interval_time = 5

    def _position(self, param):
        for td in param.find_all('a'):
            print("职位名称："+td.string)
            self._city(td.string)

    def _save_excel(self, jobs_list):

        if os.path.exists(JOB_EXCEL_PATH):
            df = pd.read_excel(JOB_EXCEL_PATH)
            df = df.append(jobs_list)
        else:
            df = pd.DataFrame(jobs_list)

        writer = pd.ExcelWriter(JOB_EXCEL_PATH)
        # columns参数用于指定生成的excel中列的顺序
        df.to_excel(excel_writer=writer, columns=['职位薪资', '职位所属公司', '职位发布地址', '职位所需经验', '职位所需学历'], index=False,
                    encoding='utf-8', sheet_name='Sheet')
        writer.save()
        writer.close()


    def _get_job_info(self, jobHtml):
        #print(jobHtml)
        #print(type(jobHtml))
        soup = BeautifulSoup(jobHtml, 'html.parser')
        #print(type(soup))

        jobs_list = []

        for job_item in soup.find_all('li'):
            #print(job_item)
            #print(job_item.find_all('div'))
            salary = job_item.find_all('div')[1].find('span').text
            company = job_item.find_all('div')[2].string
            address = job_item.find_all('div')[3].find_all('em')[0].string
            experience = job_item.find_all('div')[3].find_all('em')[1].string
            education = job_item.find_all('div')[3].find_all('em')[2].string
            print("职位薪资： " + salary)
            print("职位所属公司： " + company)
            print("职位发布地址： " + address)
            print("职位所需经验： " + experience)
            print("职位所需学历： " + education)
            jobs = {'职位薪资': salary,
                    '职位所属公司': company,
                    '职位发布地址': address,
                    '职位所需经验': experience,
                    '职位所需学历': education}
            jobs_list.append(jobs)

        return jobs_list


    def _spider_page(self, jobUrl):
        pageNum = 1
        jobHtml = "this is job html"
        while (jobHtml !=''):
            #print(jobUrl)
            jobUrl = jobUrl.replace("page=pageNum","page="+str(pageNum))
            #print(jobUrl)
            pageNum += 1
            try:
                jobRes = requests.get(jobUrl, headers=self.header)
                jobSoup = BeautifulSoup(jobRes.text, 'html.parser')
                #print(jobSoup.prettify())
                jobData = json.loads(str(jobSoup))
                #print(jobData)
                if jobData['code'] == 0 :
                    jobHtml = jobData['zpData']['html']
                    #print(jobHtml)
                    jobs_list = self._get_job_info(jobHtml)
                    self._save_excel(jobs_list)
                    time.sleep(self.interval_time)
                else:
                    jobHtml = ''
            except Exception as e:
                print('获取职位招聘地址失败，原因：'+jobUrl)
                raise e
            finally:
                jobUrl = jobUrl.replace("page="+str(pageNum-1),"page=pageNum")


    def _city(self,query):
        try:
            res = requests.get(self.city_url, headers=self.header)
            soup = BeautifulSoup(res.text, 'html.parser')
            #print(soup.prettify())
            cityData = json.loads(str(soup))
            #print(cityData)
            if cityData['code'] == 0 :
                for cityList in cityData['zpData']['cityList']:
                    #print(cityList['subLevelModelList'])
                    for cityInfo in cityList['subLevelModelList']:
                        print("招聘职位所在地址："+cityInfo['name'])
                        jobUrl = self.jobs_url + "?page=pageNum&city=" + str(cityInfo['code']) + "&query=" + query
                        #print("招聘职位Url："+ jobUrl)
                        self._spider_page(jobUrl)
        except Exception as e:
            print('获取职位招聘地址失败，原因：')
            raise e


    def spider(self):
        url = 'https://s.taobao.com/search?q=%E5%85%85%E6%B0%94%E5%A8%83%E5%A8%83&imgfile=&js=3&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191005&ie=utf8&bcoffset=4&p4ppushleft=%2C48&s=88&ntoffset=4&ajax=true'
        verify_send_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '244',
            'Cookie': 'thw=cn; v=0; cna=9cL+FWAutmgCAdvtcHjmSmqt; t=744396ed33b9755e6920c68d12863f40; cookie2=160a508f76b47e83a5fa79bc34be223e; _tb_token_=e93eb4ebeee13; unb=2404263474; uc3=nk2=Vvzz5I6YlWgDX14V8wjW&lg2=URm48syIIVrSKA%3D%3D&vt3=F8dByuHTL6zy6PajxR4%3D&id2=UUwQkjjq8GMS9Q%3D%3D; csg=1abd801a; lgc=520%5Cu8E2E%5Cu8D77%5Cu811A%5Cu5C16%5Cu7D22%5Cu543B; cookie17=UUwQkjjq8GMS9Q%3D%3D; dnk=520%5Cu8E2E%5Cu8D77%5Cu811A%5Cu5C16%5Cu7D22%5Cu543B; skt=03c28aec4e54e274; existShop=MTU3MDI4NDgwMA%3D%3D; uc4=nk4=0%40VHrFrnDrlCIjhdm9EUNsmDUHDvb4SmcsDO0%3D&id4=0%40U27Pv2pHv6CG4b5lBCK%2F1E7RBhdq; tracknick=520%5Cu8E2E%5Cu8D77%5Cu811A%5Cu5C16%5Cu7D22%5Cu543B; _cc_=URm48syIZQ%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=%E5%90%BB4c; _nk_=520%5Cu8E2E%5Cu8D77%5Cu811A%5Cu5C16%5Cu7D22%5Cu543B; cookie1=BYjcMtJ44SirNTwf5FrUVCdNuq9jyuGOwxfzKKrp1j0%3D; mt=ci=3_1; enc=Vup5zMWCNFYnQo%2BxIuKUuNk3lvfs3L%2BFpr15nsXjHdZ75C%2F1LGvwq2PZD0vVQ5APq0fEsaSJL6otEiBt3gxhtA%3D%3D; _m_h5_tk=634fbc46b468deca39b5b5b0c4fed98e_1570297263446; _m_h5_tk_enc=36e4f77f0af441c66e961b264ffb47d5; hng=CN%7Czh-CN%7CCNY%7C156; swfstore=35969; uc1=cookie14=UoTbnVqcSr3sgg%3D%3D&cookie15=UtASsssmOIJ0bQ%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; whl=-1%260%260%261570290500247; isg=BPn5ltx1gHD87lzkLzRtokpICGXTBu24OUvN2BsuXyDOohk0Y1IUiSKzJObxGoXw; l=cBgUfPr4qAj5UccJBOCZhurza77TdIRAguPzaNbMi_5ap6vVqcbOkOnD1Fv6cjWd9RLB4tm2-g29-etlwluP9P--g3fP.; JSESSIONID=3878F23570F1A0E0E8EDDB17B0A707D2',
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 's.taobao.com',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        r = requests.get(url=url, headers=verify_send_headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        #html = r.text



        print(soup)




if __name__ == '__main__':
    bossZhiPin = SpiderBossZhiPin()
    bossZhiPin.spider()




