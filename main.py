import sys

#向path添加文件夹所在路径
sys.path.append(r'D:\Program Files (x86)\JetBrains\PyCharm Community Edition 5.0.4\jre\jre\bin\PycharmProjects\untitled')

import coupon,stocks,jd_review

def main():
    print('*===============请选择操作模式================*')
    print('*          (1)领取优惠券                      *')
    print('*          (2)查商品信息                      *')
    print('*          (3)查商品评价                      *')
    print('*          (0)退出                           *')
    print('*============================================*')
    do_type=input('请输入您的选择：').strip()
    if do_type=='1':
        c=coupon.Coupon()
        c.run()
        return main()
    elif do_type=='2':
        s=stocks.Stock()
        s.get_price()
        s.get_stock()
        return main()
    elif do_type=='3':
        r=jd_review.reviewer()
        r.run_review()
        return main()
    elif do_type=='0':
        print('退出成功')
    else:
        print('您的输入有误，请重新输入！')
        return main()

if __name__=='__main__':
    main()