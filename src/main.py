
    # 标准库导入
import os   进口的
import re   进口再保险
import sys   导入系统
import time   导入的时间
from datetime import datetime, timedelta从datetime导入datetime， timedelta

# 本地化和时区处理
from zoneinfo import ZoneInfo 从zoneinfo导入zoneinfo

# 网络请求和配置文件处理
import requests   进口的请求
import configparser   进口configparser

# 邮件处理库
import   进口smtplib smtplib
from从电子邮件。导入header email.header import Header
from从email.mime.text导入mime文本 email.mime.text import MIMEText

# 获取环境变量
def get_env_variable(name):def get_env_variable(名称):Def get_env_variable(name)：def get_env_variable(name):def get_env_variable(namespace):def get_env_variable(name)：戴夫get_env_variable(名字):戴夫get_env_variable(名称):戴夫get_env_variable(名字):戴夫get_env_variable(名字):戴夫get_env_variable (namespace):戴夫get_env_variable(名字):
    try:   试一试:
        return os.environ[name]   返回os.environ   约[名称]
    except KeyError:   除了KeyError:
        print(f"环境变量 {name} 未设置，请检查配置。")
        sys.exit(1)

def fetch_notion_users(api_key, database_id):Def fetch_notion_users(api_key, database_id)：
    url = f"https://api.notion.com/v1/databases/{database_id}/query"Url = f"https://api.notion.com/v1/databases/f"https://api.notion.com/v1/databases/{database_id}/query"；
    headers = {   Headers = {
        "Authorization": f"Bearer {api_key}","Authorization": f"Bearer {api_key}",
        "Notion-Version": "2021-05-13","Notion-Version": "2021-05-13",
        "Content-Type": "application/json""Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)响应=请求。帖子(url,头=标题)
    if response.status_code != 200:如果响应。status_code != 200:
        raise Exception("Failed to fetch data from Notion API: " + response.text) 引发异常（"；从概念API获取数据失败："； response.text）
    data = response.json()
    users = []
    for result in data.get("results", []):
        user_data = {}
        properties = result.get("properties", {})
        # 假设姓名字段名为 "Name"，邮箱字段名为 "Email"
        name = properties.get("Name", {}).get("title", [{}])[0].get("text", {}).get("content")
        email = properties.get("Email", {}).get("email")
        if name and email:   如果姓名和电子邮件：
            user_data["name"] = name   User_data ["name"] =名称
            user_data["email"] = email
            users.append(user_data)User_data ["email"] = email
    return users

def send_message(sender, password, server, receiver, text):
    msg = MIMEText(text, 'html', 'utf-8')   如果姓名和电子邮件：
    subject = '今日科技早报'
    msg['Subject'] = Header(subject, 'utf-8')  # type: ignore # 邮件主题
    attempt = 1   尝试次数= 1
    while attempt <= 3:   当尝试<；= 3时：while attempt <= 3:   当尝试<；= 3时：while attempt <= 3:   当尝试<；= 3时：while attempt <= 3:   当尝试<；= 3时：
        try:   试一试:
            smtpobj = smtplib.SMTP_SSL(server)Smtpobj = smtplib。SMTP_SSL(服务器)
            smtpobj.connect(server)   smtpobj.connect(服务器)
            smtpobj.login(sender, password)smtpobj。登录(发送者、密码)
            smtpobj.sendmail   进口的(sender, receiver, msg.as_string())smtpobj。Sendmail（发件人，收件人，msg.as_string()）
            print("邮件发送成功")
            smtpobj.quit()  # 关闭服务器
            return True   还真
        except smtplib.SMTPException:smtplib除外。SMTPException:
            print("尝试发送邮件失败，进行下一次尝试...")
            time.sleep(3)
            attempt += 1   尝试次数= 1   attempt  = 1   尝试次数= 1
    print("达到最大尝试次数，无法发送邮件")
    return False   返回假

def is_news_sorted(news_string):
    """检查新闻是否已经排序（通过检查是否包含(sorted)标记）"""
    # 检查是否包含排序后的标记(sorted)
    return "(sorted)" in news_string返回"；（排序）"；在news_stringreturn "(sorted)" in   在 news_string返回"；（排序）"；在news_stringreturn "(sorted)" in news_string返回"；（排序）"；在news_stringreturn "(sorted)" in   在 news_string返回"；（排序）"；在news_string

def simple_filter_news(matches):def simple_filter_news(匹配):
    """简单过滤新闻，返回前25条高质量新闻"""
    from news_filter import filter_news_list, should_filter_news从news_filter导入filter_news_list， should_filter_news
    
    # 将matches转换为(title, url)格式
    news_list = [(match[0], match[1]) for match in matches]News_list = [(match[0], match[1]) for match in matches]
    
    # 使用通用过滤函数过滤新闻
    filtered_news = filter_news_list(news_list)Filtered_news = filter_news_list（新闻列表）
    
    # 进一步过滤掉标题过短的新闻
    quality_filtered = [(title, url) for title, url in filtered_news if len(title) >= 10]
    
    # 如果过滤后的新闻不足25条，从原始新闻中补充（但仍要排除广告和金额相关新闻）
    if len(quality_filtered) < 25:
        # 从原始新闻中找到未被包含且通过基本过滤的新闻
        for title, url in news_list:
            if (title, url) not in quality_filtered and len(quality_filtered) < 25:
                # 确保补充的新闻也通过基本过滤
                if not should_filter_news(title):
                    quality_filtered.append((title, url))
    
    # 转换回原始格式
    return [(title, url) for title, url in quality_filtered[:25]]

def format_news(news_string):
    # 使用正则表达式提取链接和标题
    pattern = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, news_string)
    
    # 检查新闻是否已排序
    if is_news_sorted(news_string):
        # 如果已排序，直接取前25条
        matches = matches[:25]
    else:
        # 如果未排序，进行简单筛选
        matches = simple_filter_news(matches)
    
    formatted_news = ''
    for match in matches:
        title = match[0]
        link = match[1]
        formatted_link = '<p><a href="{}">{}</a></p>'.format(link, title)
        formatted_news += formatted_link
    return formatted_news

def message(name, formatted_news):
    # 使用用户的名字来创建个性化问候
    greeting = f"早上好{name}，以下是今日的科技早报"
    # 检查配置变量是否为空，如果为空则设置为空字符串
    start_notification_text = start_notification if start_notification else ''
    end_notification_text = end_notification if end_notification else ''
    end_comment_text = end_comment if end_comment else ''
    text = f"""
    <h2>{greeting}</h2>
    <p>{start_notification_text}</p>
    <div>{formatted_news}</div>
    <p>{end_notification_text}</p>
    <p>{end_comment_text}</p>
    """
    return text

def switch_to_parent_if_src():
    """检查当前目录的最后一级是否是src，如果是，则切换到上一级目录"""
    current_dir = os.getcwd()
    base_name = os.path.basename(current_dir)

    if base_name == 'src':
        parent_dir = os.path.dirname(current_dir)
        os.chdir(parent_dir)
        print(f'当前目录是 {current_dir}，切换到上一级目录: {parent_dir}')
    else:
        print(f'当前目录是 {current_dir}，无需切换')

def main():
    switch_to_parent_if_src()
    
    # # 以下部分是本地测试时使用的代码
    # from dotenv import load_dotenv
    # dotenv_path = '.env'
    # load_dotenv(dotenv_path)
    # # 以上部分是本地测试时使用的代码
    
    # 创建一个ConfigParser对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('notifications.ini')
    # 获取开头通知、结尾通知和结尾注释内容，如果不存在则设置为空字符串
    global start_notification, end_notification, end_comment
    start_notification = config.get('开头通知', 'content', fallback='')
    end_notification = config.get('结尾通知', 'content', fallback='')
    end_comment = config.get('结尾注释', 'content', fallback='')

    tz = ZoneInfo('Asia/Shanghai')
    now = datetime.now(tz)
    yesterday = now - timedelta(days=1)
    yesterday_day = yesterday.strftime("%d")
    yesterday_year_month = yesterday.strftime("%Y-%m")
    yesterday_folder_path = f"news_archive/{yesterday_year_month}"
    yesterday_news_filename = f"{yesterday_folder_path}/{yesterday_day}.md"

    # 检查昨日新闻文件是否存在
    if not os.path.exists(yesterday_news_filename):
        print(f"{yesterday_news_filename} 不存在，跳过发送邮件")
        sys.exit(0)

    with open(yesterday_news_filename, 'r') as f:
        yesterday_news = f.read()

    formatted_news = format_news(yesterday_news)

    if not formatted_news:
        print("没有新闻条目，结束程序运行")
        sys.exit(0)

        try:
        sending_account = get_env_variable("SENDING_ACCOUNT")sending_account = get_env_variable（" sending_account "）
        sending_password = get_env_variable("SENDING_PASSWORD")sending_password = get_env_variable（sending_password "）
        server = get_env_variable("SERVER")server = get_env_variable（" server "）
        receiver_email = get_env_variable("RECEIVER_EMAIL")
    except Exception as e:   例外情况如下：
        print("推送消息失败，发生了一个未处理的异常:", e)
        sys.exit(1)

    personalized_message = message("读者", formatted_news)
    success = send_message(sending_account, sending_password, server, receiver_email, personalized_message)
    if not success:
        print("邮件发送失败")
    else:   其他:
        print("邮件发送成功")

    
    # # 以下部分是我本地测试时使用的代码
    # send_message(sending_account, sending_password, server,'nowscott@qq.com',message('NowScott', formatted_news))
    # # 以上部分是我本地测试时使用的代码

if __name__ == "__main__":
    main()
