## 接口参数的组成
接口参数分成两部分:公共参数和api参数,这些参数都要放在query里
### 1. 公共参数
公共参数指的是调用任意api都要上传的参数,有如下几个:

- keyid
- timestamp  :10位数的时间戳(精确到秒)
- signaturenonce  :每次请求都要生成一个唯一id,例如bson的objectid
- service  :调用的api的名称
- signature  :签名,签名规则下面会讲到
- method  :http请求方法,'GET','PUT','DELETE','POST'其中之一

### 2. api参数
各个api所要求的参数,例如 /sms/sender/identifying_code_sender 这个api要求 to 和 identifying_code 这两个参数

## 接口调用
### 1. 生成请求的参数
    dic={
        'to': '18030255113',
        'identifying_code': 'binbin',
        'service': '/sms/sender/identifying_code_sender' ,
        'keyid': 'LTAIpQAJHrAE6J9z',
        'keysecret': 'iXtiK9jz6KOE2Oa6VUOmlp8CxwPUVG',
        'method': 'GET'
    }
### 3. 将字典按照key排序,然后将排序后的字典的key和value进行urlencode后用'='链接起来,再将生成的结果按顺序用 '&' 连接,之后再将生成的结果进行urlencode,然后在将用 '&',示例python代码如下:
    string_to_sign=reduce(lambda x, y: x + '&' + y, [quote(i) + '=' + quote(dic[i]) for i in sorted(dic)])
    其中quote是起到urlencode的作用

### 4. 将得到的字符串用hmac-sha1加密,再用b64encode得到公共参数signature
    sign_key = keysecret.encode()
    sign_value = string_to_sign.encode()
    sign_method = sha1
    signature = b64encode(hmac.new(sign_key, sign_value, sign_method).digest()).decode()
    dic['signature'] = signature
    # keyid='LTAIpQAJHrAE6J9z', keysecret='iXtiK9jz6KOE2Oa6VUOmlp8CxwPUVG'
### 5. 拼接请求的字符串
    qs=reduce(lambda x, y: x + '&' + y, [quote(i) + '=' + quote(dic[i]) for i in sorted(dic)])
### 6. 调用接口
    requests.get('http://127.0.0.1?'+qs)
### 7. 生成请求字符串完整代码如下:
    from hashlib import sha1
    from functools import reduce
    from bson import ObjectId
    from urllib.parse import quote
    from base64 import b64encode
    import time
    import hmac
    from models.models import DB, Key


    def get_query_string(par=None, keyid=None, keysecret=None, service=None, http_method='GET'):
        #par应该传入api参数组成的字典
        dic = {
            'keyid': str(keyid),
            'timestamp': str(int(time.time())),
            'signaturenonce': str(ObjectId()),
            'service': str(service),
            'method': http_method
        }
        dic.update(par)
        string_to_sign = reduce(lambda x, y: x + '&' + y, [quote(i) + '=' + quote(dic[i]) for i in sorted(dic)])
        # sign------------------------------------------------------------------------------------------
        sign_key = keysecret.encode()
        sign_value = string_to_sign.encode()
        sign_method = sha1
        signature = b64encode(hmac.new(sign_key, sign_value, sign_method).digest()).decode()
        dic['signature'] = signature
        # ------------------------------------------------------------------------------------------------
        return reduce(lambda x, y: x + '&' + y, [quote(i) + '=' + quote(dic[i]) for i in sorted(dic)])

