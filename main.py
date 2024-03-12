# -*- coding: utf-8 -*-
# @Author : 艾登科技
# @Email : aidencaptcha@gmail.com
# @Address : https://github.com/aidencaptcha

# ZhihuLoginSpider 知乎-登录/注册实战案例

# YidunCaptchaBreak 网易易盾验证码

# api 地址

# * [YidunCaptchaBreak](https://github.com/aidencaptcha/YidunCaptchaBreak)


import time
import json
import requests
from loguru import logger
logger.debug(r"""
    _     _      _                ____                _          _
   / \   (_)  __| |  ___  _ __   / ___|  __ _  _ __  | |_   ___ | |__    __ _ 
  / _ \  | | / _` | / _ \| '_ \ | |     / _` || '_ \ | __| / __|| '_ \  / _` |
 / ___ \ | || (_| ||  __/| | | || |___ | (_| || |_) || |_ | (__ | | | || (_| |
/_/   \_\|_| \__,_| \___||_| |_| \____| \__,_|| .__/  \__| \___||_| |_| \__,_|
                                              |_|
@Author : 艾登科技
@Email : aidencaptcha@gmail.com
@Address : https://github.com/aidencaptcha
@Description : API需求请在邮箱联系 aidencaptcha@gmail.com
""")


def aiden_api(proxy, referer, id):
    """ 艾登科技-易盾接入API """
    aiden_url = f"http://api.xxx.com/yiduncap?proxy={proxy}&referer={referer}&id={id}"
    response = requests.request("GET", aiden_url, timeout=30)
    data = json.loads(response.text)
    V2_validate = data['result']['V2_validate']
    return V2_validate


global_cookies = {
}

def zhihu_login(proxy):
    referer = 'https://www.zhihu.com/signin'
    id = 'ffccaa537da544269b4c9c1dc84dcb73'
    V2_validate = aiden_api(proxy, referer, id)
    # logger.debug(f'validate: {V2_validate}')
    url = "https://www.zhihu.com/api/v3/oauth/captcha/v2"
    payload = {
        'ticket': json.dumps({"validate": V2_validate})
    }
    headers = {
        'authority': 'www.zhihu.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'x-zse-93': '101_3_3.0',
        'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTb8tu60FqK6P0E49y-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Ie8FL7AtqM6O1VDQyQ6nxrRPCHukMoCXBEgOsiRP0XL2ZUBXmDDV9qhnyTXFMnXcTF_ntRueThXe_e4rfz9L1JDoBxceBSDuC9CHpc8XmRgY06rpLxDoOfCoMwqwMArOfwGVPvHgLmgY0DvxMJqx8EGt9HCLZVv9LAqtBFgVM5JLfo6e999cOrRYGvrS0XrXGhhCGHbH0M6X0JrNfuUFMLGNGZuY02exMEgx1bwpfWGwMQRHG6Lc1HvO04qfzhhCMriC1x9VGhreMabOYpCS9oMC0kbLCgwNCzwLpNbLflho0CvLCabx_NrS1fcnOxUuqpqo9wreB3BgCoDV86igMT93Gt9LqbhN_CDemiuoM1XHCwrVC',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'x-zse-96': '2.0_r8L/igfbeuMApAxzacnzyW7xjl4Fqua3/cg1Ss=rHADKyfHy54Vu9mTmIZDHdSzY',
        'x-requested-with': 'fetch',
        'x-xsrftoken': '93c89deb-bffe-4e75-9974-4a4c142bc455',
        'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://www.zhihu.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zhihu.com/signin?next=%2F',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    response = requests.request("PUT", url, headers=headers, cookies=global_cookies, data=payload)
    global_cookies.update(response.cookies.get_dict())
    logger.debug(response.text)
    if 'success' in response.text:
        if response.json()['success']:
            return V2_validate, response.cookies.get_dict()
        else:
            return
    else:
        return


if __name__ == '__main__':
    count = 0
    for i in range(100):
        proxy = 'http://127.0.0.1:7890'
        res = zhihu_login(proxy)
        if res:
            validate, cookies = res
            logger.debug(f"""
【知乎-登录/注册实战案例】
validate: {validate[:100] + '**********脱敏处理**********' + validate[-100:]}
cookies: {json.dumps(cookies)[:100] + '**********脱敏处理**********' + json.dumps(cookies)[-100:]}
调用次数: {count+1}""")
            count += 1

        time.sleep(1) # 速度限制