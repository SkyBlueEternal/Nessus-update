# coding: utf-8
# /usr/bin/env python
import os
import re
import json
import time
import random
import requests
from tqdm import tqdm


class Nessus:
    def __init__(self):
        self.req = requests.Session()
        self.name = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5))

    def ten_mail(self):
        self.req.request(
            method="GET",
            url="https://mailtemp.top/mailbox?name={0}".format(self.name),
            verify=True
        )
        print("临时申请邮箱为:{0}@mailtemp.top".format(self.name))
        return "{0}@mailtemp.top".format(self.name)

    def ten_mail_2(self):
        time.sleep(10)
        tmp2 = self.req.request(
            method="GET",
            url="https://mailtemp.top/api/v1/mailbox/{0}".format(self.name),
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "Referer": "https://mailtemp.top/mailbox?name=",
                "Accept-Language": "zh-CN,zh;q=0.9"
            },
            verify=True
        )
        b = tmp2.text
        b2 = json.loads(b)
        tmp3 = self.req.request(
            method="GET",
            url="https://mailtemp.top/mailbox/{0}/{1}".format(self.name, b2[0]["id"]),
            headers = {
                      "Accept": "application/json, text/javascript, */*; q=0.01",
                      "X-Requested-With": "XMLHttpRequest",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                      "Referer": "https://mailtemp.top/mailbox?name=",
                      "Accept-Language": "zh-CN,zh;q=0.9"
            },
        )
        key = re.findall("[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", tmp3.text)
        key = key[0]
        print("https://plugins.nessus.org/register.php?serial={0}".format(key))
        self.req.close()
        tmp4 = requests.get(url="https://plugins.nessus.org/register.php?serial={0}".format(key))
        tmp5 = tmp4.text.split("\n")
        print("https://plugins.nessus.org/v2/nessus.php?f=all-2.0.tar.gz&u={0}&p={1}".format(tmp5[1],tmp5[2]))
        print("开始下载文件.")
        url = "https://plugins.nessus.org/v2/nessus.php?f=all-2.0.tar.gz&u={0}&p={1}".format(tmp5[1],tmp5[2])
        response = requests.get(url, stream=True)  # (1)
        file_size = int(response.headers['content-length'])  # (2)
        dst = "all-2.0.tar.gz"
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst)  # (3)
        else:
            first_byte = 0
        if first_byte >= file_size:  # (4)
            return file_size

        header = {"Range": f"bytes={first_byte}-{file_size}"}

        pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
        req = requests.get(url, headers=header, stream=True)  # (5)
        with open(dst, 'ab') as f:
            for chunk in req.iter_content(chunk_size=1024):  # (6)
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()

    def s_Nessus(self):
        tmp = requests.post(
            url="https://zh-cn.tenable.com/products/nessus/nessus-essentials",
            data={
                "first_name": "1",
                "last_name": "1",
                "email": "{0}@mailtemp.top".format(self.name),
                "org_name": "",
                "opt_in": "on",
                "robot": "human",
                "type": "homefeed",
                "token": "",
                "country": "CN",
                "submit": "注册",
            },
            verify=True
        )
        self.ten_mail_2()

def run():
    ben = "》》》》》》Nessus 更新包下载脚本《《《《《《\r\nby:柠檬菠萝"
    print(ben)
    print("*开始执行程序，保障网络通畅，如有问题请反馈。")
    a = Nessus()
    a.s_Nessus()

