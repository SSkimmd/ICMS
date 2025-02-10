import asyncio
import logging
import time
import json as Json
import sys
import os
import ssl
import util
import importlib


from extension import Extension
from threading import Thread
from flask import Flask, request
from flask import Response
from datatypes import Device, Connection, User, Callback
from flask_cors import CORS
from stream import Server as StreamServer

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.extensions: map[str, Extension] = {}
        self.server: StreamServer = None

        self.start_time = 0

        CORS(self.app, resources={
            "/*": {
                "origins": "*"
            }
        })

        self.app.add_url_rule("/login", view_func=self.user_login, methods=["POST"])
        self.app.add_url_rule("/register", view_func=self.user_register, methods=["POST"])
        self.app.add_url_rule("/devices/add", view_func=self.add_device, methods=["POST"])
        self.app.add_url_rule("/devices", view_func=self.get_devices, methods=["GET"])
        self.app.add_url_rule("/device", view_func=self.call_device, methods=["POST"])
        self.app.add_url_rule("/connections", view_func=self.get_connections, methods=["GET"])
        self.app.add_url_rule("/extension", view_func=self.get_extension, methods=["POST"])
        self.app.add_url_rule("/extensions", view_func=self.call_function, methods=["POST"])
        self.app.add_url_rule("/extensions", view_func=self.get_extension_config, methods=["GET"])
        self.app.add_url_rule("/serverLog", view_func=self.server_log, methods=["POST"])
        self.app.add_url_rule("/serverInfo", view_func=self.server_info, methods=["GET"])
        self.app.add_url_rule("/restart", view_func=self.restart, methods=["GET"])
        self.app.add_url_rule("/stop", view_func=self.stop, methods=["GET"])
        self.app.add_url_rule("/start", view_func=self.start, methods=["GET"])

    def init_extensions(self):
        with open("./settings/extensions.json") as file:
            json = Json.loads(file.read())

            if not "extensions" in json: return

            for extension in json["extensions"]:
                name = list(extension.keys())[0]

                if "lib" not in extension[name] or "enabled" not in extension[name]: 
                    print("ERROR: Extension Multiple Key Error")
                    continue
                
                if not extension[name]["enabled"]:
                    print(f'Skipping Extension: {name}')
                    continue

                lib = extension[name]["lib"]

                try:
                    if sys.modules.get(lib):
                        sys.modules.pop(lib)
                        print(f'Reimporting: {name}')
                    new_module = importlib.import_module(lib) 
                    new_extension: Extension = new_module.initialise(self.server)
                    self.extensions[name] = new_extension
                    print(f'Started Extension: {name}')
                except:
                    print(f'Failed To Import Module Name: {name}')
                    continue
        return
    
    async def user_login(self):



        return Response("", status=200)
    
    async def user_register(self):
        data = request.get_json()

        if 'username' not in data:
            return(400, 'ERROR: Key Error (username)')
        
        if 'password' not in data:
            return(400, 'ERROR: Key Error (password)')

        username = data["username"]
        user = User(username)


        return(200, f'SUCCESS: Registered {username}')
    
    async def add_device(self):
        data = request.get_json()
        
        connection_name = data["connection_name"]
        name = data["device_name"]
        type = data["device_type"]

        response = await self.server.add_device(connection_name, Device(name, type))

        status_code = response[0]
        response_data = response[1]

        return Response(status=status_code, response=Json.dumps({ "response": response_data }))
    
    async def get_devices(self):
        devices = self.server.devices
        devices_response = {}
        for device in devices:
            connection: Connection = await self.server.get_connection(connection_name=device)
            
            if connection is None:
                continue
            
            devices_response[device] = {
                "device_name": devices[device].device_name,
                "device_type": devices[device].device_type,
                "device_endpoints": connection.endpoints
            }

        return Response(status=200, response=Json.dumps(devices_response))
    
    async def call_device(self):
        data = request.get_json()
        response = await self.server.call_device(data)

        return Response(status=200, response=Json.dumps(response))
    
    async def get_connections(self):
        connections = self.server.connections
        connections_response = []
        for connection in connections:
            if connections[connection].device is not None:
                continue

            name = connections[connection].connection_name
            connections_response.append(name)

        return Response(status=200, response=Json.dumps(connections_response))
    
    async def get_extension(self):
        data = request.get_json()

        if "module" not in data:
            return Response(status=400, response=Json.dumps({}))

        name = data["module"]
        response = await self.server.get_extensions(name)

        status_code = response[0]
        response_data = response[1]

        if status_code == 400:
            self.server.logger.error(response_data)

        return Response(status=status_code, response=Json.dumps(response_data))
    
    async def call_function(self):
        data = request.get_json()
        response = await self.server.call_function(data)

        status_code = response[0]
        response_data = response[1]

        if status_code == 400:
            self.server.logger.error(str(response_data))

        return Response(status=status_code, response=Json.dumps(response_data))
    
    async def get_extension_config(self):
        extensions: dict[str, dict] = { }
        with open("settings/extensions.json") as file:
            json = Json.loads(file.read())
            for extension in json["extensions"]:
                name = list(extension.keys())[0]
                extensions[name] = {
                    "enabled": extension[name]["enabled"],
                    "lib": extension[name]["lib"] 
                }
            
        return Response(response=Json.dumps({ "extensions": extensions }), 
        status=200, 
        mimetype='application/json')   
    
    async def server_log(self):
        data = request.get_json()
        lines = int(data["lines"])
        out = ""
        log = util.reverse_readline("logs/log.txt")
        count = 0
        for line in log:
            if count == lines:
                break

            if line[0:2] == "  ":
                continue

            out += line + "\n"
            count += 1
        return Response(response=out, status=200, mimetype='application/json')  
       
    async def server_info(self):
        uptime = time.time() - self.start_time

        server_running = False
        if self.server is not None:
            server_running = self.server.running            

        return Response(
            response=Json.dumps({
                "server_running": server_running,
                "server_uptime": round(uptime, 2)
            }), 
            status=200, 
            mimetype='application/json'
        )
    
    def restart(self):
        return Response("Restarting...", 200)
    def stop(self):
        asyncio.run(self.server.close())
        return Response("Stopping...", 200)   
    def start(self):
        self.init_extensions()
        self.server = StreamServer(ssl_context=None)
        self.server.extensions = self.extensions

        self.start_time = time.time()
        asyncio.run(self.server.start())

        return Response("Starting...", 200)

def StartWebServer():
    server = WebServer()

    server_thread = Thread(target=server.start, daemon=True)
    server_thread.start()

    return server.app