
import urllib.request
import json
import time
import datetime

PATH = "./api_server_info.json"

def get_dict_from_jsonf(path):
	dict_ret = dict()
	with open(path, "r") as f:
		dict_ret = json.load(f)
	return dict_ret

def api_update(host, port, timeout=int(60), is_test=int(0)):
    url = "http://{}:{}/update".format(host, port)
#    print(url)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as res:
        body = res.read()
    return body


UPDATE_INTERVAL = 20

def main():
    dict_api_server_info = get_dict_from_jsonf(path=PATH)
    host = dict_api_server_info["host"]
    port = dict_api_server_info["port"]

    dt_update = datetime.datetime.now() + datetime.timedelta(seconds=UPDATE_INTERVAL)
    while True:
        dt_now = datetime.datetime.now()
        # API: update ===
        if dt_now > dt_update:
            try:
                res = api_update(host=host, port=port, is_test=int(0), timeout=int(300))
                dt_update = datetime.datetime.now() + datetime.timedelta(seconds=UPDATE_INTERVAL)
                print("kicked: api update, next: {}".format(dt_update))

            except Exception as e:
                print("error at update")
                print(e)
        
        time.sleep(10)

if __name__ == '__main__':
    print("start: tool info server data aquisition scheduler")
    try:
        main()
    except Exception as e:
        print(e)
