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
            latest_file_first_line = f.readline().strip()
        if realtime_hot_top != latest_file_first_line:
            print("Hot search has changed")
            compare_content(log_path, realtime_hot_str, to_email, from_email, password,smtp_server,port)
        else:
            print("Hot search has not changed")
    # time.sleep(10) # 10 seconds

if __name__ == '__main__':
    url = 'https://weibo.com/ajax/side/hotSearch'
    log_path='./log'
    config_path='./config.json'
    main()
    pass