# -*- coding:utf-8 -*-


import requests
import time
import base64
import rsa
import json
import binascii

def get_user_name(name):

    return base64.b64encode(name.encode('utf-8'))


def get_password(password, n, e='10001'):

    pub_key = rsa.PublicKey(int(n, 16), int(e, 16))
    crypto = rsa.encrypt(password.encode('utf8'), pub_key)
    return binascii.b2a_hex(crypto)



def save_cookies(cookies):
    cookies_data = requests.utils.dict_from_cookiejar(cookies)
    with open("cookie_json", "a+") as f:
        f.writelines(json.dumps(cookies_data) + "\n")
    return cookies_data


class WeiboLogin:

    def __init__(self, user, password):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        self.session = requests.session()
        self.user = user
        self.password = password

    def get_request(self, url):

        res = self.session.get(url, headers=self.headers)
        assert res.status_code == 200, "failed to request {}, status_code is {}".format(url, res.status_code)
        return res

    def pre_login(self):

        pre_url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&' \
                  'su=&rsakt=mod&client=ssologin.js(v1.4.19)&_={}'.format(int(time.time() * 1000))
        res = self.get_request(pre_url)
        pre_data_dict = res.json()
        nonce = pre_data_dict['nonce']
        pubkey = pre_data_dict['pubkey']
        rsakv = pre_data_dict['rsakv']
        return nonce, pubkey, rsakv

    def sso_login(self, nonce, rsakv, sp, su):

        form_data = {'encoding': 'UTF-8',
                     'entry': 'weibo',
                     'from': '',
                     'gateway': '1',
                     'nonce': nonce,
                     'pagerefer': 'https://login.sina.com.cn/crossdomain2.php?action=logout&'
                                  'r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
                     'prelt': '22',
                     'pwencode': 'rsa2',
                     'qrcode_flag': 'false',
                     'returntype': 'META',
                     'rsakv': rsakv,
                     'savestate': '7',
                     'servertime': int(time.time()),
                     'service': 'miniblog',
                     'sp': sp,
                     'sr': '1920*1080',
                     'su': su,
                     'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&'
                            'callback=parent.sinaSSOController.feedBackUrlCallBack',
                     'useticket': '1',
                     'vsnf': '1'}
        login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_={}'.format(
            int(time.time() * 1000))
        res = self.session.post(login_url, headers=self.headers, data=form_data)
        return res.text

    def login(self):
        nonce, pubkey, rsakv = self.pre_login()

        name = get_user_name(self.user)
        password = str(int(time.time())) + '\t' + str(nonce) + '\n' + str(self.password)
        password = get_password(password, pubkey)

        self.sso_login(nonce, rsakv, password, name)
        return save_cookies(self.session.cookies)

def get_cookies(user_name, pass_word):
    weibo_login = WeiboLogin(user_name, pass_word)
    cookies = weibo_login.login()
    return cookies

if __name__ == '__main__':
    cookie = get_cookies("*****", "*****")
    with open("test.log", "a+") as f:
        f.writelines(json.dumps(cookie))
