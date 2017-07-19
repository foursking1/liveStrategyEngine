#! /usr/bin/python
# -*- encoding: utf-8 -*-
# @Author: DZF
import hashlib
import hmac
import time
from collections import OrderedDict
from urllib.parse import urlencode
import accountConfig
import urllib
import urllib.parse
import urllib.request

import requests

# Nonce Length
JUBI_NONCE_LENGHT = 12

ACCESS_KEY = accountConfig.JUBI["CNY_1"]["ACCESS_KEY"]
SECRET_KEY = accountConfig.JUBI["CNY_1"]["SECRET_KEY"]
SERVICE_API = accountConfig.JUBI["CNY_1"]["SERVICE_API"]


def getMd5Hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def generate_signature(msg, private_key):
    msg = msg.encode(encoding='UTF8')
    k = getMd5Hash(private_key.encode(encoding='UTF8')).encode(encoding='UTF8')
    signature = hmac.new(k, msg, digestmod=hashlib.sha256).hexdigest()
    return signature


def reformat_params(params, private_key):
    orderDict = OrderedDict(params)
    param_str = urlencode(orderDict)
    #param_str = '&'.join(['%s=%s' % (str(k), str(v)) for (k, v) in orderDict.items()])
    signature = generate_signature(param_str, private_key)
    orderDict['signature'] = signature
    return orderDict


def get2api(pParams, method):
    request_url = SERVICE_API + method
    return httpGet(request_url, pParams)


def send2api(pParams, method):
    pParams['key'] = ACCESS_KEY
    pParams['nonce'] = int(time.time() * 1000)
    pParams = reformat_params(pParams, SECRET_KEY)
    request_url = SERVICE_API + method
    print(pParams)
    # if (extra):
    #     for k in extra:
    #         v = extra.get(k)
    #         if (v != None):
    #             pParams[k] = v
                # pParams.update(extra)
    return httpRequest(request_url, pParams)


'''
生成签名
'''


def createSign(params):
    params['secret_key'] = SECRET_KEY
    params = sorted(params.items(), key=lambda d: d[0], reverse=False)
    message = urllib.parse.urlencode(params)
    message = message.encode(encoding='UTF8')
    m = hashlib.md5()
    m.update(message)
    m.digest()
    sig = m.hexdigest()
    return sig


def httpGet(url, params):
    print(url)
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }

    postdata = urllib.parse.urlencode(params)
    # postdata = postdata.encode('utf-8')
    response = requests.get(url, postdata, headers=headers, timeout=20)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)

        raise Exception("httpPost failed, detail is:%s" % response.text)

'''
request
'''


def httpRequest(url, params):
    print(url)
    '''
    postdata = urllib.parse.urlencode(params)
    postdata = postdata.encode('utf-8')

    fp = urllib.request.urlopen(url, postdata, timeout = 20)
    if fp.status != 200:
        return None
    else:
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        return mystr
    '''
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }

    postdata = urllib.parse.urlencode(params)
    # postdata = postdata.encode('utf-8')
    response = requests.post(url, postdata, headers=headers, timeout=20)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)

        raise Exception("httpPost failed, detail is:%s" % response.text)


if __name__ == '__main__':
    pass
