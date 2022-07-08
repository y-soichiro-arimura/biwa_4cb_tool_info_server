from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from typing import List, Dict, Optional
import datetime
import json
import urllib.request
import uvicorn

from config.config import ServerConf
from utils.client import (
    api_auto_ope_cycle_count,
    api_machine_list,
    api_tool_info_plc)


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
    
    def machine_ip_list(self):
        return list(self.tool_status.keys())
    
    def is_valid_machine_ip(self, machine):
        if machine in self.tool_status.keys():
            return True
        else:
            False
    
    def get_tool_status(self, machine=None):
        if machine:
            if not self.is_valid_machine_ip(machine=machine):
                return False
            return {machine: self.tool_status[machine]}
        else:
            return self.tool_status
    
    def force_update(self, machine):
        if not self.is_valid_machine_ip(machine=machine):
            return False
        self.tool_status[machine]["status"] = api_tool_info_plc(machine=machine)[machine]
        return True
    
    def update(self):
        # check target machine ---
        target = list()
        auto_ope_cycle_count = api_auto_ope_cycle_count()
        for k, v in auto_ope_cycle_count.items():
            if k == "last_access":
                continue
            if (0 < v["aoc_fin_count"]) and self.is_valid_machine_ip(machine=k):
                target.append(k)
        # update ---
        for m in target:
            self.tool_status[m]["status"] = api_tool_info_plc(machine=m)[m]
            self.tool_status[m]["timestamp"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return None

print("start: tool_status_handler")
tsh = ToolStatusHandler()
app = FastAPI()

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

@app.get('/machine_ip_list')
def machine_ip_list():
    ret = {"machine_ip_list": tsh.machine_ip_list()}
    return JSONResponse(
        content=ret, 
        status_code=status.HTTP_200_OK)

@app.get('/force_update/{machine}')
def force_update(machine):
    ret = tsh.force_update(machine=machine)
    return JSONResponse(
        content={'force_update_status': ret}, 
        status_code=status.HTTP_200_OK)

@app.get('/tool_status')
def tool_status():
    return JSONResponse(
        content=tsh.tool_status, 
        status_code=status.HTTP_200_OK)

@app.get('/tool_status/{machine}')
def tool_status(machine):
    return JSONResponse(
        content=tsh.get_tool_status(machine=machine), 
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
        

host = ServerConf.HOST
port = ServerConf.PORT

print(f"server is working at {host}:{port}")
uvicorn.run(
    app=app, 
    host=host, 
    port=port)