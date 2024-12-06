import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from datetime import datetime
import os

def hot_search(url):
    
    response = requests.get(url)
    if response.status_code != 200:
        return None
    results = response.json()['data']
    realtime_hot = results['realtime']
    realtime_hot_df = pd.DataFrame(realtime_hot)['word']
    realtime_hot_str=realtime_hot_df.to_string(index=False)
    realtime_hot_top = (realtime_hot_str.splitlines()[0]).split(' ')[-1]
    return realtime_hot_str,realtime_hot_top

def send_email(email_subject, email_body, to_email_list,from_email,password,smtp_server,port):
    for i in range(len(to_email_list)):
        to_email=to_email_list[i]
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = email_subject

        msg.attach(MIMEText(email_body, 'plain'))

        try:
            server = smtplib.SMTP_SSL(smtp_server, port)
            # server.ehlo()
            # server.starttls() ## when ssl it is no need

            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            now = datetime.now().strftime('%Y-%m-%d-%H-%M')
            print(f"Time:{now},Status:Email sent successfully")
        except Exception as e:
            print(f"Time:{now},Status:Failed to send email: {e}")

def check_path(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def get_config(config_path):
    config_data = json.load(open(config_path))
    to_email = config_data['target']
    from_email = config_data['from_email']
    password = config_data['password']
    port=config_data['port']
    smtp_server=config_data['smtp']
    pushplus_token=config_data['pushplus_token']
    return to_email, from_email, password,smtp_server,port,pushplus_token,config_data['webhook']

def get_latest_file(file_path):
    files=os.listdir(file_path)
    if len(files)==0:
        return None
    latest_file=None
    latest_time=None
    for file in files:
        try:
            file_time = datetime.strptime(file, '%Y-%m-%d %H:%M_weibo_hot_search.txt')
            if latest_time is None or file_time > latest_time:
                latest_time = file_time
                latest_file = file
        except ValueError:
            continue
    latest_file_path=os.path.join(file_path,latest_file)
    return latest_file_path


def send_text(webhook, content, mentioned_list=None, mentioned_mobile_list=None):
    header = {
                "Content-Type": "application/json",
                "Charset": "UTF-8"
                }
    data ={
 
        "msgtype": "text",
        "text": {
            "content": content
            ,"mentioned_list":mentioned_list
            ,"mentioned_mobile_list":mentioned_mobile_list
        }
    }
    data = json.dumps(data)
    info = requests.post(url=webhook, data=data, headers=header)
    

def send_md(webhook, content):
    header = {
                "Content-Type": "application/json",
                "Charset": "UTF-8"
                }
    data ={
 
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    data = json.dumps(data)
    info = requests.post(url=webhook, data=data, headers=header)
    print(f"Time:{datetime.now().strftime('%Y-%m-%d %H:%M')},Status:Webhook sent successfully")

def pushplus_push(pushplus_token, title, content):
    try:
        data={
            "token": pushplus_token,
            "title": title,
            "content": content
        }
        url='http://www.pushplus.plus/send'
        body=json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type':'application/json'}
        response = requests.post(url, data=body, headers=headers)
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        if response.status_code == 200:
            print(f"Time:{now},Status:Pushplus sent successfully")
        else:
            print(f"Time:{now},Status:Failed to send pushplus")
        pass
    except Exception as e:
        print(f"Time:{now},Status:Failed to send pushplus: {e}")

def compare_content(log_path,realtime_hot_str,to_email,from_email,password,smtp_server,port,pushplus_token=None,webhook_key=None):
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        output_path_name=f'{now}_weibo_hot_search.txt'
        output_path=os.path.join(log_path,output_path_name)
        with open(output_path, 'w') as f:
            f.write(realtime_hot_str)
        send_email(f'微博热搜榜({now})', realtime_hot_str, to_email,from_email,password,smtp_server,port)
        pushplus_push(pushplus_token=pushplus_token, title=f'微博热搜榜({now})', content=realtime_hot_str)
        send_text(webhook_key, content=f'微博热搜榜({now})\n{realtime_hot_str}')
        # send_md(webhook_key, content=f'# 微博热搜榜({now})\n{realtime_hot_str}')

def hot_top_history_manager(new_hot_top,hot_top_history_path):
    max_lines=24
    new_hot_top_n=new_hot_top+'\n'
    try:
        with open(hot_top_history_path, "r") as f:
            lines = f.readlines()
        if new_hot_top_n in lines:
            print(f"{new_hot_top} is existing")
            return 1
        else:
            lines.append(new_hot_top_n)
            if len(lines) > max_lines:
                lines = lines[-max_lines:]
            with open(hot_top_history_path, "w") as f:
                f.writelines(lines)
            print(f"add {new_hot_top} succeed!")
            return 0
    except FileNotFoundError:
        with open(hot_top_history_path, "w") as f:
            f.write(new_hot_top_n)
        print(f"history file is not exist, created just now and add {new_hot_top}")
        return 0
    except Exception as e:
        print(f"error code:{e}")
        return 2
    pass

