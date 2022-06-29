import json
import urllib.request



aoc_count_api_info = {
    "host": "192.168.0.10",
    "port": 8080}

tool_info_plc_api_info = {
    "host": "192.168.0.144",
    "port": 30000}

def api_auto_ope_cycle_count(
        host=aoc_count_api_info["host"], 
        port=aoc_count_api_info["port"]):
    url = "http://{}:{}/auto_ope_cycle_count".format(host, port)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            body = res.read()
        data = json.loads(body)
        data = json.loads(data)
    except Exception as e:
        print(e)
        data = list()
    return data

def api_machine_list(
        host=tool_info_plc_api_info["host"], 
        port=tool_info_plc_api_info["port"]):
    url = "http://{}:{}/machines".format(host, port)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            body = res.read()
        data = json.loads(body)
        data = data["machine_list"]
    except Exception as e:
        print(e)
        data = list()
    return data

def api_tool_info_plc(
        machine,
        host=tool_info_plc_api_info["host"], 
        port=tool_info_plc_api_info["port"],):
    url = "http://{}:{}/tool_status/{}".format(host, port, machine)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            body = res.read()
        data = json.loads(body)
    except Exception as e:
        print(e)
        data = {machine: "not available from tool_into_plc"}
    return data