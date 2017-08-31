# coding=utf-8
from bs4 import BeautifulSoup
import re

import login
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
# sessions = login.login()
#
# my_order_response = sessions.get('https://order.jd.com/center/list.action', allow_redirects=False)
# my_order = BeautifulSoup(my_order_response.text, 'lxml')
# my_order_tbodys = my_order.find_all('tbody')
# for my_order_tbody in my_order_tbodys:
#     print my_order_tbody
#
# scripts = my_order.find_all('script')[3]
# # print scripts
# orderWareIds = re.findall(r"\[\'orderWareIds\'\] = (.+?);", scripts.text)[0].strip()
# orderWareTypes = re.findall(r"\[\'orderWareTypes\'\] = (.+?);", scripts.text)[0].strip()
# orderIds = re.findall(r"\[\'orderIds\'\] = (.+?);", scripts.text)[0].strip()
# orderTypes = re.findall(r"\[\'orderTypes\'\] = (.+?);", scripts.text)[0].strip()
# orderSiteIds = re.findall(r"\[\'orderSiteIds\'\] = (.+?);", scripts.text)[0].strip()
#
# getOrderProductInfoFormData = {
#     'orderWareIds': orderWareIds,
#     'orderWareTypes': orderWareTypes,
#     'orderIds': orderIds,
#     'orderTypes': orderTypes,
#     'orderSiteIds': orderSiteIds
# }
# orderProductInfo = sessions.post('https://order.jd.com/lazy/getOrderProductInfo.action', data=getOrderProductInfoFormData, allow_redirects=False)


my_order = BeautifulSoup(open('order.html').read(), "html.parser")
my_order_tbodys = my_order.find_all('tbody')


# my_order_tbody = my_order_tbodys[0]
# print my_order_tbody
# id = my_order_tbody['id']

def getTbodyInfo(my_order_tbody):
    a_list = my_order_tbody.find_all('a')
    for a in a_list:
        if '订单详情' in a.text:
            details_url = 'https:' + a['href']
            if 'details.jd.com' in details_url:
                print details_url
            elif 'home.jd.hk' in details_url:
                print '海外购'
            # orderId = id.encode().strip('tb-')  # 订单号
            # trs = my_order_tbody.find_all('tr', attrs={'class': 'tr-bd'})
            # for tr in trs:
            #     if tr.get('id') is None:
            #         continue
            #     productId = tr.find('span', attrs={'class': 'o-match J-o-match'})['data-sku']  # 商品id
            #     goodsNumber = tr.find('div', attrs={'class': 'goods-number'}).text.encode('utf-8').strip().strip('x')
            # dealtime = my_order_tbody.find('span', attrs={'class': 'dealtime'})['title']  # 订单时间
            # amount_div = my_order_tbody.find('div', attrs={'class': 'amount'})
            # amount_str = amount_div.contents[1].text.encode('utf-8')
            # amount = re.findall(r'¥(.+)', amount_str)[0]
            # pay_type = amount_div.contents[5].text.encode('utf-8')
            # print dealtime
            # print amount
            # print pay_type


for my_order_tbody in my_order_tbodys:
    id = my_order_tbody['id']
    if 'parent' in id:
        orderId = id.encode().strip('parent-')
        getParentOrderListData = {
            'pin': '14759289890_p',
            'parentIds': orderId
        }
        # parentOrderList = sessions.post('https://order.jd.com/lazy/getParentOrderList.action', data=getParentOrderListData).content.decode('gbk').encode('utf-8')
        children_tbodys = my_order.find_all('tbody', attrs={"class": id})
        for tbody in children_tbodys:
            order_status = tbody.find('span', attrs={'class': 'order-status'}).text.encode('utf-8').strip()
            if order_status != '已完成':
                continue
            getTbodyInfo(tbody)
            # orderId = id.encode().strip('tb-')  # 订单号
            # trs = tbody.find_all('tr', attrs={'class': 'tr-bd'})
            # for tr in trs:
            #     if tr.get('id') is None:
            #         continue
            #     productId = tr.find('span', attrs={'class': 'o-match J-o-match'})['data-sku']  # 商品id
            #     goodsNumber = tr.find('div', attrs={'class': 'goods-number'}).text.encode('utf-8').strip().strip('x')
            # dealtime = tbody.find('span', attrs={'class': 'dealtime'})['title']  # 订单时间
            # amount_div = tbody.find('div', attrs={'class': 'amount'})
            # amount_str = amount_div.contents[1].text.encode('utf-8')
            # amount = re.findall(r'¥(.+)', amount_str)
            # pay_type = amount_div.contents[5].text.encode('utf-8')
            # print dealtime
            # print amount
            # print pay_type
    else:
        if my_order_tbody.get('class') is not None and 'parent' in my_order_tbody['class'][1]:
            continue
        order_status = my_order_tbody.find('span', attrs={'class': 'order-status'}).text.encode('utf-8').strip()
        if order_status != '已完成':
            continue
        getTbodyInfo(my_order_tbody)
