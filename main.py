import time
from model import *

def main():
    check_path(log_path)
    to_email, from_email, password,smtp_server,port,pushplus_token,webhook_key = get_config(config_path=config_path)
    realtime_hot_str,realtime_hot_top = hot_search(url)
    realtime_hot_str=realtime_hot_str.replace(" ","")
    latest_file_path=get_latest_file(log_path)
    status_code_hot_top=hot_top_history_manager(new_hot_top=realtime_hot_top,hot_top_history_path=hot_top_log)
    if status_code_hot_top==1:
        now = datetime.now().strftime('%Y-%m-%d-%H-%M')
        print(f"Time:{now}, Statues:Hot search has not changed")
        pass
    elif status_code_hot_top==0:
        lines = realtime_hot_str.split('\n')
        result = ""
        for i, line in enumerate(lines):
            result += f"{i+1}.{line}\n"
        realtime_hot_str=result
        now = datetime.now().strftime('%Y-%m-%d-%H-%M')
        print(f"Time:{now}, Statues:Hot search has changed")
        compare_content(log_path, realtime_hot_str,
                to_email, from_email, password,smtp_server,port,
                pushplus_token,webhook_key)

        # if latest_file_path is None :
        #     print(f"Time:{datetime.now().strftime('%Y-%m-%d-%H-%M')}, Statues:First time to get hot search")
        #     compare_content(log_path, realtime_hot_str, 
        #     to_email, from_email, password,smtp_server,port,
        #     pushplus_token,webhook_key)
        # else:
        #     with open(latest_file_path, 'r') as f:
        #         latest_file_first_line = (f.readline().strip()).split(' ')[-1]
        #     if "1."+realtime_hot_top== latest_file_first_line:
        #         now = datetime.now().strftime('%Y-%m-%d-%H-%M')
        #         print(f"Time:{now}, Statues:Hot search has not changed")
        #         pass
        #     else:
        #         now = datetime.now().strftime('%Y-%m-%d-%H-%M')
        #         print(f"Time:{now}, Statues:Hot search has changed")
        #         compare_content(log_path, realtime_hot_str,
        #         to_email, from_email, password,smtp_server,port,
        #         pushplus_token,webhook_key)
    else:
        print("error!")
        pass
    time.sleep(60) # 10 seconds


if __name__ == '__main__':
    url = 'https://weibo.com/ajax/side/hotSearch'
    log_path='/root/zhuzilan/github/reptiles4weibo/log'
    config_path='/root/zhuzilan/github/reptiles4weibo/config.json'
    hot_top_log='/root/zhuzilan/github/reptiles4weibo/hot_top_history.txt'
    main()
    pass