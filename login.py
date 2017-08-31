# coding=utf-8
import os
import urllib
import urllib2

import requests
import hashlib

import time
from bs4 import BeautifulSoup


def login():
    image_header = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'authcode.jd.com',
        'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    }

    sessions = requests.session()
    login_page = sessions.get('https://passport.jd.com/new/login.aspx', allow_redirects=False)
    login_soup = BeautifulSoup(login_page.text, 'lxml')
    login_postinfo = login_soup.find_all('form', attrs={'id': 'formlogin'})[0].find_all('input')
    uuid = login_soup.find_all('input', attrs={'id': 'uuid'})[0]['value']
    _t = login_soup.find_all('input', attrs={'name': '_t'})[0]['value']
    # # 下载验证码图片：
    checkPicUrl = login_soup.find_all("div", id="o-authcode")[0].find_all("img")[0]['src2']
    timestamp = int(round(time.time() * 1000))
    imageUrl = 'https:' + checkPicUrl + '&yys=' + timestamp.__str__()
    req = sessions.get(imageUrl, headers=image_header)
    checkPic = open("checkPic.jpg", "w")
    checkPic.write(req.content)
    checkPic.close()
    # 调用mac系统的预览(图像查看器)来打开图片文件
    os.system('open /Applications/Preview.app/ checkPic.jpg')
    checkCode = raw_input("请输入弹出图片中的验证码：")
    for input_info in login_postinfo:
        if len(input_info['value']) == 5:
            str1 = input_info['name']
            str2 = input_info['value']
            break
    m2 = hashlib.md5()
    m2.update('Luo030440')
    post_info = {
        'uuid': uuid,
        'loginname': '14759289890',
        'loginpwd': m2.hexdigest(),
        'machineCpu': '',
        'machineDisk': '',
        'machineNet': '',
        'nloginpwd': m2.hexdigest(),
        str1: str2,
        '_t': _t,
        'authcode': checkCode}
    content = sessions.post('http://passport.jd.com/uc/loginService', data=post_info, allow_redirects=False)
    return sessions
