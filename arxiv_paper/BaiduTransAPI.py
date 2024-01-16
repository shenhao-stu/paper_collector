# coding=utf-8
import http.client
import hashlib
import urllib
import random
import json

def get_translate(query, from_l, to_l, appid='', secretKey=''):
    myurl = '/api/trans/vip/translate'
    appid = 'appid'
    secretKey = 'secretKey'

    fromLang = from_l   #原文语种
    toLang = to_l   #译文语种
    salt = random.randint(32768, 65536)
    q= query
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
    except Exception as e:
        result = '翻译API没钱了'
        
    return result
