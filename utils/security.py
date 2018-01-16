from hashlib import sha1
from functools import reduce
from bson import ObjectId
from urllib.parse import quote
from base64 import b64encode
import time
import hmac
from models.models import DB, Key


def get_quory_string(par=None, keyid=None, keysecret=None, service=None, http_method='GET'):  # 生成quory
    dic = {
        'keyid': str(keyid),
        'timestamp': str(int(time.time())),
        'signaturenonce': str(ObjectId()),
        'service': str(service)
    }
    dic.update(par)
    qs = reduce(lambda x, y: x + '&' + y, [quote(i) + '=' + quote(dic[i]) for i in sorted(dic)])
    string_to_sign = http_method + '&%2F&' + quote(qs)
    # sign------------------------------------------------------------------------------------------
    sign_key = keysecret.encode()
    sign_value = string_to_sign.encode()
    sign_method = sha1
    signature = b64encode(hmac.new(sign_key, sign_value, sign_method).digest()).decode()
    dic['signature'] = signature
    # ------------------------------------------------------------------------------------------------
    return reduce(lambda x, y: x + '&' + y, [quote(i) + '=' + quote(dic[i]) for i in sorted(dic)])


def verify_quory(r):  # 输入是flask的request,需要完善对timestamp和signaturenonce的利用
    dic = r.args.to_dict()
    http_method = r.method

    signature_ = dic.pop('signature')
    qs = reduce(lambda x, y: x + '&' + y, [quote(i) + '=' + quote(dic[i]) for i in sorted(dic)])
    string_to_sign = http_method + '&%2F&' + quote(qs)
    # sign------------------------------------------------------------------------------------------
    sign_key = DB.query(Key).filter(Key.keyid == dic['keyid']).first().keysecret.encode()
    sign_value = string_to_sign.encode()
    sign_method = sha1
    signature = b64encode(hmac.new(sign_key, sign_value, sign_method).digest()).decode()
    # ------------------------------------------------------------------------------------------------
    if signature == signature_:
        return 1
    else:
        return 0


if __name__ == '__main__':
    print(get_quory_string(par={'to': '18030255113', 'text': 'nihao'}, service='/sms/sender/any_text_sender',
                           keyid='LTAIpQAJHrAE6J9z', keysecret='iXtiK9jz6KOE2Oa6VUOmlp8CxwPUVG',http_method='PUT'))
