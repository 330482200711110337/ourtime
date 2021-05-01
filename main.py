import re
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
class Corona(object):

    def __init__(self):
        self.home_url='https://ncov.dxy.cn/ncovh5/view/pneumonia'
        self.headers={"User -Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36 Edg/86.0.622.68"}

    def get_content_from_url(self,url):
        txt=requests.get(url=url,headers=self.headers).content.decode()
        return txt

    def parse_home_page(self,txt,id):
        #解析
        soup=BeautifulSoup(txt,"lxml")
        script=soup.find(id=id)
        txt=script.string
        jst=re.findall(r'\[.+\]',txt)[0]
        data=json.loads(jst)
        return data

    def lastdaygtC(self):
        homepage=self.get_content_from_url(self.home_url)
        last_dat_covid=self.parse_home_page(homepage,'getAreaStat')
        self.save_js(last_dat_covid,'lastdayC.json')

    def save_js(self,jst,path):
        #存储
        with open (path,"w") as f:
            json.dump(jst,f)
    def allcovid19(self):
        #每天
        tester=[]
        with open("lastday.json","r") as f:
            lastday=json.load(f)

        for country in tqdm(lastday,'采集数据中'):

            station_url=country['statisticsData']
            station_url_json=self.get_content_from_url(station_url)
            station=json.loads(station_url_json)['data']

            for oneday in station:
                oneday["provinceName"]=country["provinceName"]
                oneday["countryShortCode"] = country["countryShortCode"]

            tester.append(station)

        self.save_js(tester,"lastday_covid19.json")

        print("采集成功")

    def lastdaygt(self):

        homepage=self.get_content_from_url(self.home_url)
        last_dat_covid=self.parse_home_page(homepage,'getListByCountryTypeService2true')
        self.save_js(last_dat_covid,'lastday.json')

    def allcovid19China(self):
        #每天

        tester=[]
        with open("lastdayC.json","r") as f:
            lastday=json.load(f)

        for country in tqdm(lastday,'采集数据中'):

            station_url=country['statisticsData']
            station_url_json=self.get_content_from_url(station_url)
            station=json.loads(station_url_json)['data']

            for oneday in station:
                oneday["provinceName"]=country["provinceName"]
                #oneday["countryShortCode"] = country["countryShortCode"]

            tester.append(station)
        self.save_js(tester,"lastday_covid19C.json")

        print("采集成功")

    def run(self):

        print("-"*50)

        while True:
            n=input("What do you want to do of COVID-19?If you want to search for China,1\nelse if you want to search for world,2")

            if n=='1':

                self.lastdaygtC()
                self.allcovid19China()

            elif n=='2':

                self.lastdaygt()
                self.allcovid19()

            else:
                print("input again")

            print("-" * 50)

            m=input("Want you break(Y/N)?")

            if m=="Y":
                break

if __name__=='__main__':
    user=Corona()
    user.run()