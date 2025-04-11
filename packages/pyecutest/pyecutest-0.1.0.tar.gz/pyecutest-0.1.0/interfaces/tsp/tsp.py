'''
Author: guwenjun1 guwenjun1@xiaomi.com
Date: 2024-02-22 19:07:12
LastEditors: guwenjun1 guwenjun1@xiaomi.com
LastEditTime: 2024-03-26 17:58:40
FilePath: \AutoVehicleTest\base\tsp.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import time,hashlib,json,requests


if __name__=='__main__':
    ak = "edd9a392e67a42bfb2a76a2574f4b81d"
    sk = "b58551d1e35c4cd598e7f17d23b16ccf"
    url = "https://pre-inner.tsp.mioffice.cn/vehicle-monitor-service/miCarStandard/realData/viewData"
    path_url = "/vehicle-monitor-service/miCarStandard/realData/viewData"
    params = {
        "collectTimeEnd": "2024-03-26 17:44:30",
        "collectTimeStart": "2024-03-26 17:40:30",
        "signals": [
            "PwrModSts",
            "ExtrLtgStsPosLiFrnt",
            "ExtrLtgStsPosLiRe",
            "HvBattSoCAct",
            "AmbTRaw",
            "ABSErrDetd"
        ],
        "limit": 0,
        "vin": "LNBSC1VK6PB101030",
        "type": 1
    }

    json_dict = json.dumps(params, sort_keys=True, separators=(',', ':'))

    str2sign = path_url + "POST" + json_dict
 
    timestamp = str(int(time.time()) * 1000)

    # 待签名串 = AccessKey+ SecretKey + 时间戳（毫秒） + StringToSign
    sign = ak + sk + timestamp + str2sign
    #先将签名字符串转化成二进制再用sha512算法计算得到16进的签名
    hash_object = hashlib.sha512(sign.encode())
    signature = hash_object.hexdigest()
    payload = json.dumps(params, sort_keys=True, separators=(',', ':'))

    headers = {
        'accesskey': ak,
        'signature': signature,
        'timestamp': timestamp,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
