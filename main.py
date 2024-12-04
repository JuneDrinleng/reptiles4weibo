import time
from model import *

def main():
    check_path(log_path)
    to_email, from_email, password,smtp_server,port = get_config(config_path=config_path)
    realtime_hot_str,realtime_hot_top = hot_search(url)
    latest_file_path=get_latest_file(log_path)
    if latest_file_path is None :
        compare_content(log_path, realtime_hot_str, to_email, from_email, password,smtp_server,port)
    else:
        with open(latest_file_path, 'r') as f:
            latest_file_first_line = (f.readline().strip()).split(' ')[-1]
        if realtime_hot_top.strip() == latest_file_first_line.strip():
            now = datetime.now().strftime('%Y-%m-%d-%H-%M')
            print(f"Time:{now}, Statues:Hot search has not changed")
        else:
            now = datetime.now().strftime('%Y-%m-%d-%H-%M')
            print(f"Time:{now}, Statues:Hot search has changed")
            compare_content(log_path, realtime_hot_str, to_email, from_email, password,smtp_server,port)
    time.sleep(60) # 10 seconds

if __name__ == '__main__':
    url = 'https://weibo.com/ajax/side/hotSearch'
    log_path='/root/zhuzilan/github/reptiles4weibo/log'
    config_path='/root/zhuzilan/github/reptiles4weibo/config.json'
    main()
    pass