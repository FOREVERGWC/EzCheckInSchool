import time
import json
import requests
import random
import datetime

# sectets字段录入
deptid = input()
stuNo = input()
username = input()
sckey = input()

# 时间判断
now = (time.localtime().tm_hour + 8) % 24
if (now >= 6) & (now < 8):
    templateid = "clockSign1"
    customerAppTypeRuleId = 146
elif (now >= 12) & (now < 14):
    templateid = "clockSign2"
    customerAppTypeRuleId = 147
elif (now >= 21) & (now <= 22):
    templateid = "clockSign3"
    customerAppTypeRuleId = 148
else:
    print("现在是%d点%d分，将打卡早间档测试" %(now,time.localtime().tm_min))
    templateid = "clockSign1"
    customerAppTypeRuleId = 146

# 随机温度(36.2~36.4)
a = random.uniform(36.2, 36.4)
temperature = round(a, 1)

sign_url = "https://reportedh5.17wanxiao.com/sass/api/epmpics"

jsons = {
    "businessType": "epmpics",
    "method": "submitUpInfoSchool",
    "jsonData": {
        "deptStr": {
            "deptid": deptid,
            "text": round(time.time() * 20)
        },
        "areaStr": {"streetNumber":"","street":"长椿路辅路","district":"中原区","city":"郑州市","province":"河南省","town":"","pois":"河南工业大学(莲花街校区)","lng":113.544407 + random.random()/10000,"lat":34.831014 + random.random()/10000,"address":"中原区长椿路辅路河南工业大学(莲花街校区)","text":"河南省-郑州市","code":""},
        "reportdate": round(time.time() * 30),
        "customerid": 43,
        "deptid": deptid,
        "source": "app",
        "templateid": templateid,
        "stuNo": stuNo,
        "username": username,
        "userid": round(time.time() * 50),
        "updatainfo": [
            {
                "propertyname": "temperature",
                "value": temperature
            },
            {
                "propertyname": "symptom",
                "value": "无症状"
            }
        ],
        "customerAppTypeRuleId": customerAppTypeRuleId,
        "clockState": 0
    },
}

# 提交打卡与结果判定
flag = 0
for i in range(1,5):
    response = requests.post(sign_url, json=jsons)
    utcTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    cstTime = utcTime.strftime("%H时%M分%S秒")
    if response.status_code == 200:
        flag=1
        break
    else:
        time.sleep(60)
print(response.text)
if flag == 1:
    if response.json()["msg"] == '成功':
        msg = cstTime + "打卡成功"
    else:
        msg = cstTime + "打卡异常"
else:
    msg = cstTime + "网络错误打卡失败"

print(msg)

# 微信通知
title = msg
result = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
content = f"""
```
{result}
```

"""
data = {
    "text": title,
    "desp": content
}
req = requests.post(sckey, data=data)
