'''
Author: guwenjun1 guwenjun1@xiaomi.com
Date: 2024-03-06 21:01:11
LastEditors: guwenjun1 guwenjun1@xiaomi.com
LastEditTime: 2024-03-26 17:54:54
FilePath: \AutoVehicleTest\base\tsp_request.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests,hashlib,json,time
from urllib.parse import urlparse


class TspRequest:
    def __init__(self,url,ak,sk,vid):
        self.url = url
        self.ak = ak
        self.sk = sk
        self.vid = vid


    def get_tsp_info(self, signal):
        self.path_url = self.get_url_path(self.url)
        params = {
            "signalNameList": [signal],
            "vid": "LNBQXJGG2YWG8YMA9",
            "reqSource":"ms-vehicledata-rt",
        }

        json_dict = json.dumps(params, sort_keys=True, separators=(',', ':'))

        str2sign = self.path_url + "POST" + json_dict
    
        timestamp = str(int(time.time()) * 1000)

        # 待签名串 = AccessKey+ SecretKey + 时间戳（毫秒） + StringToSign
        sign = self.ak + self.sk + timestamp + str2sign
        #先将签名字符串转化成二进制再用sha512算法计算得到16进的签名
        hash_object = hashlib.sha512(sign.encode())
        signature = hash_object.hexdigest()
        payload = json.dumps(params, sort_keys=True, separators=(',', ':'))

        headers = {
            'accesskey': self.ak,
            'signature': signature,
            'timestamp': timestamp,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", self.url, headers=headers, data=payload)

        return response.text
    
    def get_url_path(self,url):
        return urlparse(url).path
    # start_time、end_time为旧的接口需要的请求参数，新接口已弃用
    def check_tsp_info(self, signal):
        res = self.get_tsp_info(signal)
        print(res)
        if res:
            respData = json.loads(res)["respData"]
            value = respData[0]["signalValue"]
            return value
        else:
            return None
