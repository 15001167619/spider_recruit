import requests

import json
import time

s = requests.Session()


class TianYanChaSend:

    def __init__(self):
        """ 公司投递api """
        self.tyc_send_api = 'https://www.tianyancha.com/contact/sendCard/companyId.json'
        """ 地区代码列表 """
        self.companyName = "北京时代创信科技有限公司"
        """ 地区代码列表 """
        self.contactNumber = "13811491190"
        """ 地区代码列表 """
        self.intention = "您好，我们是互联网定制服务商，如果有业务需要，请联系我们。"
        """ 姓名 """
        self.realName = "马洪宇"
        """ 姓名 """
        self.type = 10
        # 请求超时时间
        self.timeout = 3
        self.companyId = 3

    def send_data(self):

        verify_send_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '244',
            'Content-Type': 'application/json; charset=UTF-8',
            'Cookie': 'ssuid=5285871275; TYCID=636019c0d45211e985baefd6bd263e3b; undefined=636019c0d45211e985baefd6bd263e3b; _ga=GA1.2.1545809170.1568178593; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25221%2522%252C%2522contactNumber%2522%253A%252213811491190%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%252286%2525%2522%252C%2522state%2522%253A%25225%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522surday%2522%253A%2522179%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252298%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25226%2522%252C%2522claimUnread%2522%253A%25222%2522%252C%2522claimPoint%2522%253A%25221%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzgxMTQ5MTE5MCIsImlhdCI6MTU2ODI1NDQ0NywiZXhwIjoxNTk5NzkwNDQ3fQ.gjFMkM6R8yB3j_EbQSvx2CHI7mcDDeI00kd1XZVPS7Rw0jDZYoy5JCWkPIoPXhi_egg-MOJn1JViWAr9bqlmuQ%2522%252C%2522vipToTime%2522%253A%25221583670010592%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522industry%2522%253A%2522IT%257C%25E9%2580%259A%25E4%25BF%25A1%257C%25E7%2594%25B5%25E5%25AD%2590%257C%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522post%2522%253A%2522IT%257C%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%257C%25E9%2580%259A%25E4%25BF%25A1%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522claimDetailLevel%2522%253A%252218%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%2597%25B6%25E4%25BB%25A3%25E5%2588%259B%25E4%25BF%25A1%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25222%2522%252C%2522companyName%2522%253A%2522%25E5%258C%2597%25E4%25BA%25AC%25E6%2597%25B6%25E4%25BB%25A3%25E5%2588%259B%25E4%25BF%25A1%25E7%25A7%2591%25E6%258A%2580%25E6%259C%2589%25E9%2599%2590%25E5%2585%25AC%25E5%258F%25B8%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522realName%2522%253A%2522%25E9%25A9%25AC%25E6%25B4%25AA%25E5%25AE%2587%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252220%2522%252C%2522mobile%2522%253A%252213811491190%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzgxMTQ5MTE5MCIsImlhdCI6MTU2ODI1NDQ0NywiZXhwIjoxNTk5NzkwNDQ3fQ.gjFMkM6R8yB3j_EbQSvx2CHI7mcDDeI00kd1XZVPS7Rw0jDZYoy5JCWkPIoPXhi_egg-MOJn1JViWAr9bqlmuQ; aliyungf_tc=AQAAAP80ZxyezwwA6cExPUG3Qh+vZD8K; bannerFlag=undefined; csrfToken=ifMcYo5TwwbAhppZqdQWubZ9; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568189249,1568254383,1568264255,1568700976; _gid=GA1.2.272601667.1568700976; RTYCID=87605fcc70644390a3c2180e5b830c53; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568700986; CT_TYCID=7f917cb711d4453d919b43dd67ad4586; cloud_token=e9cbb7f0af8d4995a32bca4c9d7edae7; cloud_utm=dc9e616041bb4102b3a5a6085226b059',
            'Host': 'www.tianyancha.com',
            'Origin': 'https://www.tianyancha.com',
            'Referer': 'https://www.tianyancha.com/company/'+self.companyId,
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        verify_send_data = {
            'companyId': self.companyId,
            'companyName': self.companyName,
            'contactNumber': self.contactNumber,
            'intention': self.intention,
            'realName': self.realName,
            'type': 10
        }
        try:
            send_api = self.tyc_send_api.replace('companyId',str(self.companyId))
            print(send_api)
            send_data = json.dumps(verify_send_data, ensure_ascii=False)
            print(send_data)
            response = s.post(send_api, headers=verify_send_headers, data=send_data.encode(),
                              timeout=self.timeout)
            print(response)
            response.raise_for_status()
            # 从返回的页面中提取申请st码地址
        except Exception as e:
            print('发送失败，原因：'+ send_api)
            raise e




if __name__ == '__main__':
    tianYanChaSend = TianYanChaSend()

    for companyId in range(1, 10000000):
        tianYanChaSend.companyId = str(companyId)
        tianYanChaSend.send_data()
        time.sleep(tianYanChaSend.timeout)
