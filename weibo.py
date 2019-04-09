# -*- coding:utf-8 -*-


import json
import random
import time
import requests
import login

user_name = '*****'

pass_word = '******'

# mobile: user page
url_user = "https://m.weibo.cn/api/container/getIndex?uid=1939498534&luicode=10000011&lfid=1076035223052780&type=uid&value=1939498534&containerid=1076031939498534"

# url_add = "https://www.weibo.com/aj/mblog/add"

url_forward = "https://weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=ljrezero&__rnd=1553964251498"


headers_mobile = {
    "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36"
}

headers_pc = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "174",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "www.weibo.com",
    "Origin": "https://www.weibo.com",
    "Referer": "https://www.weibo.com/ljrezero/home?wvr=5.",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


forward_form_data = {

    "pic_src": "",
    "pic_id": "",
    "appkey": "",

    # m id
    "mid": "4320797209942168",
    "style_type": "1",
    "mark": "",
    # forward reason
    "reason": "test_version 0.1",
    "location": "page_100505_home",
    "pdetail": "10050561350914631",
    "module": "",
    "page_module_id": "",
    "refer_sort": "",
    "rank": "0",
    "rankid": "",
    "isReEdit": "false",
    "_t": "0"

}

add_form_data = {
    "location": "v6_content_home",
    "text": "post content",
    "appkey": "",
    "style_type": "1",
    "pic_id": "",
    "tid": "",
    "pdetail": "",
    "mid": "",
    "isReEdit": "false",
    "rank": "0",
    "rankid": "",
    "module": "stissue",
    "pub_source": "main_",
    "pub_type": "dialog",
    "isPri": "0",
    "_t": "0"
}

def get_weibo_list():
    # user profile func
    response = requests.get(url=url_user, headers=headers_mobile)
    json_data = json.loads(response.text)
    cards = json_data["data"]["cards"]
    mids = []
    # instead of top but normal one
    for i in range(1, 3):
        mid = cards[i]["mblog"]["mid"]
        mids.append(mid)
    return mids

def forward_message(mid, reason):

    forward_form_data["mid"] = mid
    forward_form_data["reason"] = reason
    response = requests.post(url=url_forward, headers=headers_pc, data=forward_form_data, cookies=cookies)
    exception = ""
    try:
        response_json = response.json()
        response_code = response_json["code"]

    except Exception as ex:
        exception = ex
        response_code = 100001

    with open("weibo_log", "a+") as f:
        f.write(mid + "\n")
        f.write(str(response_code) + "\n")
        f.write("Exception:" + str(exception) + "\n")


if __name__ == '__main__':

    mids = get_weibo_list()

    cookies = login.get_cookies(user_name, pass_word)

    random.seed()
    random_string = str(random.random()) + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    # post_new_message("test 1.0" + str(random_string))

    for mid in mids:
        time.sleep(60)
        forward_message(mid=mid, reason="reason" + str(random_string))


