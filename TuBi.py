import time
import json
import random
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.utils import formataddr

# t00ls 账号配置
username = 'twsec00'  # 帐号
password = '9022cc22c0fe15f88ff2deff900c554e'  
question_num = 5  # 安全提问 参考下面
question_answer = 'G3'  # 安全提问答案



# 选择提醒方式
notice = 1  # 0 = 钉钉  1 = 邮件 2 = 我全都要

# 如果选择钉钉通知的话 请配置下方信息
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=***' # 钉钉机器人的 webhook

# 如果选择邮件通知的话 请配置下方信息
sender = '1767207458@qq.com'  # 发件人邮箱账号
sender_pass = 'ovmbnipjrwklccae'  # 发件人邮箱密码
receiver = '15203846117@sina.cn'  # 收件人邮箱账号

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
}

def t00ls_login(u_name, u_pass, q_num, q_ans):
    

    login_data = {
        'action': 'login',
        'username': u_name,
        'password': u_pass,
        'questionid': q_num,
        'answer': q_ans
    }
    response_login = requests.post('https://www.t00ls.com/login.json', data=login_data, headers=req_headers)
    response_login_json = json.loads(response_login.text)

    if response_login_json['status'] != 'success':
        return None
    else:
        print('用户:', username, '登入成功!')
        formhash = response_login_json['formhash']
        t00ls_cookies = response_login.cookies
        return formhash, t00ls_cookies


def t00ls_sign(t00ls_hash, t00ls_cookies):
    """
    t00ls 签到函数
    :param t00ls_hash: 签到要用的 hash
    :param t00ls_cookies: 登录后的 Cookies
    :return: 签到后的 JSON 数据
    """
    sign_data = {
        'formhash': t00ls_hash,
        'signsubmit': "true"
    }
    response_sign = requests.post('https://www.t00ls.com/ajax-sign.json', data=sign_data, cookies=t00ls_cookies,headers=req_headers)
    return json.loads(response_sign.text)




def dingtalk(content):
    """
    钉钉通知函数
    :param content: 要通知的内容
    :return: none
    """
    webhook_url = webhook
    dd_headers = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    dd_message = {
        "msgtype": "text",
        "text": {
            "content": f'T00ls 签到通知\n{content}'
        }
    }

    r = requests.post(url=webhook_url, headers=dd_headers, data=json.dumps(dd_message))


def mail(content):
    """
    邮件通知函数
    :param content: 要通知的内容
    :return: none
    """
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["T00ls 签到提醒", sender])
    msg['To'] = formataddr(["", receiver])
    msg['Subject'] = "T00ls 每日签到提醒"

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, sender_pass)
    server.sendmail(sender, [receiver, ], msg.as_string())
    server.quit()


def main():
    content = ''
    response_login = t00ls_login(username, password, question_num, question_answer)
    if response_login:
        response_sign = t00ls_sign(response_login[0], response_login[1])
        if response_sign['status'] == 'success':
            print('签到成功 TuBi + 1')
            content += '\n签到成功 TuBi + 1\n'

            if notice == 0:
                try:
                    dingtalk(content)
                except Exception:
                    print('请检查钉钉配置是否正确')
            elif notice == 1:
                try:
                    mail(content)
                except Exception:
                    print('请检查邮件配置是否正确')
            else:
                try:
                    dingtalk(content)
                except Exception:
                    print('请检查钉钉配置是否正确')
                try:
                    mail(content)
                except Exception:
                    print('请检查邮件配置是否正确')
        elif response_sign['message'] == 'alreadysign':
            print('已经签到过啦')
            content += '\n已经签到过啦\n'


            if notice == 0:
                try:
                    dingtalk(content)
                except Exception:
                    print('请检查钉钉配置是否正确')
            elif notice == 1:
                try:
                    mail(content)
                except Exception:
                    print('请检查邮件配置是否正确')
            else:
                try:
                    dingtalk(content)
                except Exception:
                    print('请检查钉钉配置是否正确')
                try:
                    mail(content)
                except Exception:
                    print('请检查邮件配置是否正确')
        else:
            print('出现玄学问题了 签到失败')
    else:
        print('登入失败 请检查输入资料是否正确')


if __name__ == '__main__':
    main()
