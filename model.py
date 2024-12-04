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
    realtime_hot_str=realtime_hot_df.to_string(index=True)
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
    return to_email, from_email, password,smtp_server,port

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

def compare_content(log_path,realtime_hot_str,to_email,from_email,password,smtp_server,port):
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        output_path_name=f'{now}_weibo_hot_search.txt'
        output_path=os.path.join(log_path,output_path_name)
        with open(output_path, 'w') as f:
            f.write(realtime_hot_str)
        send_email(f'微博热搜榜({now})', realtime_hot_str, to_email,from_email,password,smtp_server,port)