import requests
import json
import re
def getweather():
    print("天气查询")
    str = input("查询的城市（汉字）：")
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + str
    response = requests.get(url)
    wearher_json = json.loads(response.text)
    a = wearher_json['data']
    #当时
    lst1=["位置：" + a['city'],
          "提示：" + a['ganmao'],
          "温度：" + a['wendu'] + '℃',
          "昨天：" + a['yesterday']['date'],
          "风力：" + a['yesterday']['fl'][9:[m.start() for m in re.finditer(']', a['yesterday']['fl'])][0]],
          "风向：" + a['yesterday']['fx'],
          a['yesterday']['high'],
          a['yesterday']['low'],
          "天气：" + a['yesterday']['type']]
    for x in lst1:
        print(x)
    print()
    #后几天
    for i in range(0, 4):
        lst2=["时间：" + a["forecast"][i]['date'],
              '风力: ' + a["forecast"][i]['fengli'][9:[m.start() for m in re.finditer(']', a['yesterday']['fl'])][0]],
              '风向：' + a["forecast"][i]['fengxiang'],
              a["forecast"][i]['high'],
              a["forecast"][i]['low'],
              "天气：" + a["forecast"][i]['type']]
        for x in lst2:
            print(x)
        print()
def help():
    while True:
        getweather()
        while True:
            n = int(input("Want you break(1True/2False)"))
            if n == 1:
                print("Good bye!")
                return      #点睛之笔
            elif n == 2:
                print("let us again")
                break
            else:
                print("input again")
if __name__ == '__main__':
    help()
