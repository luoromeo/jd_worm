import requests
import time,threading
import re
from multiprocessing import Process,Pool
from get_coupon import timing


class MyInfo(object):
    def __init__(self):
        self.urls=self.get_userdata('C:\\Users\肥皂\Desktop\\url.txt')
        self.cookies=self.get_userdata('C:\\Users\肥皂\Desktop\\ck.txt')

    def get_userdata(self,file_url):
        with open(file_url,'r') as f1:
            my_lists=f1.readlines()
            data=tuple([flist.strip() for flist in my_lists])
            return data

    def set_url(self,m):
        self.url=self.urls[m-1]

    def set_headers(self,cookie):
        self.headers={
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate, sdch',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Connection':'keep-alive',
                        'Cookie':cookie,
                        'Cache-Control':'max-age=0',
                        'Upgrade-Insecure-Requests':'1',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2743.116 Safari/537.36'
                        }

    def pool_loop(self,loop_times,function):
        pool=Pool(4)
        for i in range(loop_times):
            pool.apply_async(function)
        pool.close()
        pool.join()


class GetCoupon(MyInfo):
    def get_page(self):
        s=requests.session()
        s.headers=self.headers
        try:
            r=s.get(self.url,timeout=10)
        except requests.TooManyRedirects:
            print('cookie失效，原因不明（可能是半白号，访问过快触发京东保护机制），请重新提取cookie')
        except (requests.ConnectTimeout,requests.ReadTimeout):
            print('超时重试中,若依然如此请检查网络')
        except:
            pass
        else:
            cer=re.compile('<h1 class="ctxt02"><s class="icon-redbag"></s>(.*)</h1>',flags=0)
            strlist=cer.findall(r.text)
            if not strlist:
                print('未知错误')
            else:
                print(strlist[0])

    def one_get(self,n):
        self.set_headers(self.cookies[n-1])
        self.get_page()

    def loop_one_get(self,n,loop_times):
        self.set_headers(self.cookies[n-1])
        self.pool_loop(loop_times,self.get_page)

    def all_get(self):
        for cookie in self.cookies:
            self.set_headers(cookie)
            p=Process(target=self.get_page)
            p.start()

    def loop_all_get(self,loop_times):
        for cookie in self.cookies:
            self.set_headers(cookie)
            p=Process(target=self.pool_loop,args=(loop_times,self.get_page))
            p.start()


class PostCoupon(MyInfo):
    def set_passwords(self,passwords_url):
        self.passwords=self.get_userdata(passwords_url)

    def set_password(self,n):
        self.password=self.passwords[n-1]

    def set_itemId(self,itemId):
        self.itemId=itemId

    def get_token(self):
        s=requests.session()
        r=s.get('http://vip.jd.com/bean/{}.html'.format(self.itemId))
        cer=re.compile('pageConfig.token="(.*)"')
        self.token=cer.findall(r.text)[0]
        print('token='+self.token)

    def post_page(self):
        s=requests.session()
        s.headers=self.headers
        self.data='itemId={}&password={}&token={}'.format(self.itemId,self.password,self.token)
        try:
            r=s.post('http://vip.jd.com/bean/exchangeCoupon.html',data=self.data,timeout=10)
            if '提交错误' in r.text:
                self.get_token()
                return self.post_page()
        except (requests.ConnectTimeout,requests.ReadTimeout):
            print('超时重试中,若依然如此请检查网络')
        except:
            pass
        else:
            print(r.text)

    def one_post(self,n):
        self.set_headers(self.cookies[n-1])
        self.headers['Content-Type']='application/x-www-form-urlencoded'
        self.set_password(n)
        self.post_page()

    def loop_one_post(self,n,loop_times):
        self.set_headers(self.cookies[n-1])
        self.headers['Content-Type']='application/x-www-form-urlencoded'
        self.set_password(n)
        self.pool_loop(loop_times,self.post_page)

    def all_post(self):
        for i in range(len(self.passwords)):
            self.password=self.passwords[i]
            self.set_headers(self.cookies[i])
            self.headers['Content-Type']='application/x-www-form-urlencoded'
            p=Process(target=self.post_page)
            p.start()

    def loop_all_post(self,loop_times):
        for i in range(len(self.passwords)):
            self.password=self.passwords[i]
            self.set_headers(self.cookies[i])
            self.headers['Content-Type']='application/x-www-form-urlencoded'
            p=Process(target=self.pool_loop,args=(loop_times,self.post_page))
            p.start()


class Coupon(timing.Time,GetCoupon,PostCoupon):
    def __init__(self):
        MyInfo.__init__(self)
        print('*===============请选择操作模式================*')
        print('*          (1)单个用户                       *')
        print('*          (2)所有用户                       *')
        print('*          (3)单个用户 and 循环              *')
        print('*          (4)所有用户 and 循环              *')
        print('*          (5)单个用户 and 定时              *')
        print('*          (6)所有用户 and 定时              *')
        print('*          (7)单个用户 and 定时 and 循环     *')
        print('*          (8)所有用户 and 定时 and 循环     *')
        print('*===========================================*')

    def run(self):
        name=input('请选择（1）get,（2）post（0）退出：').strip()
        if name=='1':
            name='get'
            m=int(input('请选择第m个url：'))
            self.set_url(m)
        elif name=='2':
            name='post'
            itemId=input('请输入itemId(参考http://vip.jd.com/bean/(itemId).html)：')
            self.set_itemId(itemId)
            self.get_token()
            self.set_passwords('C:\\Users\肥皂\Desktop\\password.txt')
        elif name=='0':
            print('退出成功')
            exit()
        else:
            print('输入错误，请重新输入！')
            return self.run()
        y=int(input('请选择模式（y）：'))
        if y==1:
            n=int(input('请选择第n个用户操作：'))
            eval('self.one_{}'.format(name))(n)
        elif y==2:
            eval('self.all_{}'.format(name))()
        elif y==3:
            n=int(input('请选择第n个用户操作：'))
            loop_times=int(input('请输入循环次数：'))
            eval('self.loop_one_{}'.format(name))(n,loop_times)
        elif y==4:
            loop_times=int(input('请输入循环次数：'))
            eval('self.loop_all_{}'.format(name))(loop_times)
        elif y==5:
            n=int(input('请选择第n个用户操作：'))
            self.timer()
            eval('self.one_{}'.format(name))(n)
        elif y==6:
            self.timer()
            eval('self.all_{}'.format(name))()
        elif y==7:
            n=int(input('请选择第n个用户操作：'))
            loop_times=int(input('请输入循环次数：'))
            self.timer()
            eval('self.loop_one_{}'.format(name))(n,loop_times)
        elif y==8:
            loop_times=int(input('请输入循环次数：'))
            self.timer()
            eval('self.loop_all_{}'.format(name))(loop_times)
        else:
            print('模式输入错误，请重新输入！')
            return self.run()
        time.sleep(5)

