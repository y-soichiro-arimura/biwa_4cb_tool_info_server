from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from typing import List, Dict, Optional
import datetime
import json
import urllib.request
import uvicorn


aoc_count_api_info = {
    "host": "localhost",
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
        host=aoc_count_api_info["host"], 
        port=aoc_count_api_info["port"]):
    url = "http://{}:{}/machine_list".format(host, port)
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
        data = json.loads(data)
    except Exception as e:
        print(e)
        data = list()
    return data


class ToolStatusHandler():
    '''
    assumption: datapipeline apis are available
    '''
    def __init__(self):
        self.init_tool_status()
        return None
    
    def init_tool_status(self):
        machine_list = api_machine_list()
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tool_status = dict(
            [(m, {"status": None, "timestamp": time_stamp}) for m in machine_list])
        return None
    
    def get_tool_status(self, machine=None):
        if machine:
            if not machine in self.tool_status.keys():
                return False
            return {machine: self.tool_status[machine]}
        else:
            return self.tool_status
    
    def update(self):
        # check target machine ---
        target = list()
        auto_ope_cycle_count = api_auto_ope_cycle_count()
        for k, v in auto_ope_cycle_count.items():
            if k == "last_access":
                continue
            if 0 < v["aoc_fin_count"]:
                target.append(k)
        # update ---
        for m in target:
            self.tool_status[m]["status"] = api_tool_info_plc(machine=m) # format: TBD
            self.tool_status[m]["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return None


app = FastAPI()
tsh = ToolStatusHandler()

@app.get('/server_status')
def server_status():
    return JSONResponse(
        content={'server_status': 'working'}, 
        status_code=status.HTTP_200_OK)

@app.get('/update')
def update():
    tsh.update()
    return JSONResponse(
        content={'status': 'done'}, 
        status_code=status.HTTP_200_OK)

@app.get('/tool_status')
def tool_status():
    ret = tsh.tool_status
    return JSONResponse(
        content={'tool_status': ret}, 
        status_code=status.HTTP_200_OK)

@app.get('/tool_status/{machine}')
def tool_status(machine):
    ret = tsh.get_tool_status(machine=machine)
    return JSONResponse(
        content={'tool_status': ret}, 
        status_code=status.HTTP_200_OK)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        content={'msg': 'Invalid request.'},
        status_code=status.HTTP_400_BAD_REQUEST)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):
    return JSONResponse(
        content={'msg': 'Internal server error.'},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

host = "192.168.0.10"
port = 50000

uvicorn.run(
    app=app, 
    host=host, 
    port=port)