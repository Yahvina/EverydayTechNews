import os
import re
import sys
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import configparser
import smtplib
from email.header import Header
from email.mime.text import MIMEText

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        print(f"环境变量 {name} 未设置，请检查配置。")
        sys.exit(1)

def send_message(sender, password, server, receiver, text):
    msg = MIMEText(text, 'html', 'utf-8')
    subject = '今日科技早报'
    msg['Subject'] = Header(subject, 'utf-8')
    attempt = 1
    while attempt <= 3:
        try:
            smtpobj = smtplib.SMTP_SSL(server)
            smtpobj.connect(server)
            smtpobj.login(sender, password)
            smtpobj.sendmail(sender, receiver, msg.as_string())
            print("邮件发送成功")
            smtpobj.quit()
            return True
        except smtplib.SMTPException:
            print("尝试发送邮件失败，进行下一次尝试...")
            time.sleep(3)
            attempt += 1
    print("达到最大尝试次数，无法发送邮件")
    return False

def is_news_sorted(news_string):
    return "(sorted)" in news_string

def simple_filter_news(matches):
    from news_filter import filter_news_list, should_filter_news
    news_list = [(match[0], match[1]) for match in matches]
    filtered_news = filter_news_list(news_list)
    quality_filtered = [(title, url) for title, url in filtered_news if len(title) >= 10]
    if len(quality_filtered) < 25:
        for title, url in news_list:
            if (title, url) not in quality_filtered and len(quality_filtered) < 25:
                if not should_filter_news(title):
                    quality_filtered.append((title, url))
    return [(title, url) for title, url in quality_filtered[:25]]

def format_news(news_string):
    pattern = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, news_string)
    if is_news_sorted(news_string):
        matches = matches[:25]
    else:
        matches = simple_filter_news(matches)
    formatted_news = ''
    for match in matches:
        title = match[0]
        link = match[1]
        formatted_link = '<p><a href="{}">{}</a></p>'.format(link, title)
        formatted_news += formatted_link
    return formatted_news

def message(formatted_news):
    text = f"""
    <h2>早上好，以下是今日的科技早报</h2>
    <div>{formatted_news}</div>
    """
    return   返回 text

def switch_to_parent_if_src():
    current_dir = os.getcwd()Current_dir = os.getcwd（）
    base_name = os.path.basename(current_dir)Base_name = os.path.basename（current_dir）
    if base_name == 'src':   如果base_name == 'src'：
        parent_dir = os.path.dirname(current_dir)Parent_dir = os.path.dirname（current_dir）
        os.chdir(parent_dir)
        print(f'当前目录是 {current_dir}，切换到上一级目录: {parent_dir}')
    else:   其他:   其他:
        print(f'当前目录是 {current_dir}，无需切换')

def main():
    switch_to_parent_if_src()

    tz = ZoneInfo('Asia/Shanghai')tz = ZoneInfo（'Asia/Shanghai'）
    now = datetime.now(tz)   现在= datetime.现在（tz）
    yesterday = now - timedelta(days=1)昨天=现在- timedelta（days=1）
    yesterday_day = yesterday.strftime("%d")昨天=昨天.strftime（"%d"）
    yesterday_year_month = yesterday.strftime("%Y-%m")
    yesterday_folder_path = f"news_archive/{yesterday_year_month}"
    yesterday_news_filename = f"{yesterday_folder_path}/{yesterday_day}.md"昨天文件夹_path = f"；news_archive/{昨天year_month}"；昨天的新闻文件名= f"；{昨天的文件夹_path}/{昨天的一天}.md"；
如果不是os.path.exists(yesterday_news_filename)：
    if not os.path.exists(yesterday_news_filename):昨天的新闻文件名= f"；{昨天的文件夹_path}/{昨天的一天}.md"；如果不是os.path.exists(yesterday_news_filename)：如果不是os.path.exists(yesterday_news_filename)：
        print(f"{yesterday_news_filename} 不存在，跳过发送邮件")print(f"{yesterday_news_filename} 不存在，跳过发送邮件")
        sys.exit(0)

    with open(yesterday_news_filename, 'r') as f:使用open（昨日新闻文件名，‘r’）作为f：
        yesterday_news = f.read()昨日新闻= f.read（）

    formatted_news = format_news(yesterday_news)使用open（昨日新闻文件名，‘r’）作为f：Formatted_news = format_news（昨日新闻）

    if not formatted_news:   如果不是formatted_news：
        print("没有新闻条目，结束程序运行")
        sys.exit(0)

    try:   试一试:
        sending_account = get_env_variable("SENDING_ACCOUNT")sending_account = get_env_variable（" sending_account "）
        sending_password = get_env_variable("SENDING_PASSWORD")
        server = get_env_variable("SERVER")
        receiver_email = get_env_variable("RECEIVER_EMAIL")
    except Exception as e:   例外情况如下：   例外情况如下：
        print("推送消息失败，发生了一个未处理的异常:", e)
        sys.exit(1)

    email_text = message(formatted_news)Email_text = message（formatted_news）
    success = send_message(sending_account, sending_password, server, receiver_email, email_text)成功= send_message（sending_account, sending_password, server, receiver_email, email_text）
    if not success:   如果不成功：
        print("邮件发送失败")
    else:   其他:   其他:
        print("邮件发送成功")
   如果__name__ == "__main__"；
if __name__ == "__main__":如果__name__ == "__main__"；如果__name__ == "__main__"；
    main()
