import asyncio
import logging
import time
import json as Json
import sys
import os
import ssl
import datetime

import jwt.api_jwt
import util
import importlib
import jwt
import bcrypt

from functools import wraps
from extension import Extension
from threading import Thread
from flask import Flask, request
from flask import Response
from datatypes import Device, Connection, User, Callback
from flask_cors import CORS
from stream import Server as StreamServer

async def get_user_id(token: str = None):
    logger = logging.getLogger("gunicorn.error")

    if token is None:
        return Response(status=400, response="ERROR: Authorization Header Is Missing")

    user_id = None

    try:
        decoded = jwt.api_jwt.decode(token, "secret", algorithms=["HS256"])
        user_id = decoded["user_id"]
    except:
        logger.error("ERROR: Incorrect Token Supplied")
        return None
    
    if token is None:
        logger.error("ERROR: Token Is None")
        return None
    
    if user_id is None:
        logger.error("ERROR: User ID Is None")
        return None
    
    return user_id  

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.extensions: map[str, Extension] = {}
        self.server: StreamServer = None

        self.start_time = 0
        self.users: list[User] = []

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
        self.app.add_url_rule("/server/log", view_func=self.server_log, methods=["POST"])
        self.app.add_url_rule("/server/info", view_func=self.server_info, methods=["GET"])
        self.app.add_url_rule("/restart", view_func=self.restart, methods=["GET"])
        self.app.add_url_rule("/stop", view_func=self.stop, methods=["GET"])
        self.app.add_url_rule("/start", view_func=self.start, methods=["GET"])

    def init_extensions(self):
        with open("./settings/extensions.json") as file:
            json = Json.load(file)

            for extension in json:
                ex = json[extension]

                if "lib" not in ex or "enabled" not in ex: 
                    print("ERROR: Extension Multiple Key Error")
                    continue
                
                if not ex["enabled"]:
                    print(f'Skipping Extension: {extension}')
                    continue

                lib = ex["lib"]

                try:
                    if sys.modules.get(lib):
                        sys.modules.pop(lib)
                        print(f'Reimporting: {extension}')
                    new_module = importlib.import_module(lib) 
                    new_extension: Extension = new_module.initialise(self.server)
                    self.extensions[extension] = new_extension
                    print(f'Started Extension: {extension}')
                except:
                    print(f'Failed To Import Module Name: {extension}')
                    continue
        return
    
    def requires_account(f):
        @wraps(f)
        async def decorated(self, *args, **kwargs):
            token = request.headers.get("Authorization", None)

            if token is None:
                return Response(status=400, response="ERROR: Authorization Header Not Found")
            
            if token == 'debug':
                return await f(self, *args, **kwargs)

            user_id = await get_user_id(token)
            user: User = await self.get_user(user_id=user_id)

            if user is None:
                return Response(status=400, response="ERROR: User Not Found")

            if token != user.current_token:
                return Response(status=400, response="ERROR: Incorrect Token")

            return await f(self, *args, user, **kwargs)
        return decorated    

    async def get_user(self, user_id: int = None, credentials = None):
        if user_id is not None:
            for user in self.users:
                if user.id == user_id:
                    return user

        if credentials is not None:
            for user in self.users:
                if user.username == credentials["username"]:
                    if bcrypt.checkpw(credentials["password"], user.password):
                        return user
        
        return None

    async def user_login(self):
        data = request.get_json()

        if "username" not in data:
            return Response(status=400, response="ERROR: Key Error (username)")
        
        if "password" not in data:
            return Response(status=400, response="ERROR: Key Error (password)")


        password: str = data["password"]

        credentials = {
            "username": data["username"],
            "password": password.encode()
        }

        user: User = await self.get_user(credentials=credentials)

        if user is None:
            return Response(status=400, response="ERROR: User Not Found")

        return Response(status=200, response=Json.dumps({ "token": user.current_token }), mimetype="application/json")
    
    async def user_register(self):
        data = request.get_json()

        if 'username' not in data:
            return Response(status=400, response="ERROR: Key Error (username)")
        
        if 'password' not in data:
            return Response(status=400, response="ERROR: Key Error (password)")

        username = data["username"]
        password = data["password"]

        user_id = len(self.users)
        user_token = None

        try:
            user_token = jwt.api_jwt.encode(
                {
                    "user_id": user_id,
                    "exp": datetime.datetime.now() + datetime.timedelta(days=30)
                },
                "secret",
                algorithm="HS256"
            )
        except:
            return Response(status=400, response="ERROR: Failed To Generate User Token")
        
        if user_token is None:
            return Response(status=400, response="ERROR: Failed To Generate User Token")

        
        """
            replace this with a database or load it from some external source
        """
        self.users.append(User(username, password, token=user_token, id=user_id))

        return Response(status=200, response=Json.dumps({
            "token": user_token
        }), mimetype="application/json")
    
    @requires_account
    async def add_device(self, user: User = None):   
        data = request.get_json()
        
        connection_name = data["connection_name"]
        name = data["device_name"]
        type = data["device_type"]

        response = await self.server.add_device(connection_name, Device(name, type))

        status_code = response[0]
        response_data = response[1]

        return Response(status=status_code, response=Json.dumps({ "response": response_data }), mimetype="application/json")
    
    @requires_account
    async def get_devices(self, user: User = None):
        devices = self.server.devices
        devices_response = {}

        if devices is None:
            return Response(400, response="ERROR: Device Error")

        for device in devices:
            connection: Connection = await self.server.get_connection(connection_name=device)
            
            if connection is None:
                continue
            
            devices_response[device] = {
                "device_name": devices[device].device_name,
                "device_type": devices[device].device_type,
                "device_endpoints": connection.endpoints
            }

        return Response(status=200, response=Json.dumps(devices_response), mimetype="application/json")
    
    @requires_account
    async def call_device(self, user: User = None):
        data = request.get_json()
        response = await self.server.call_device(data)

        return Response(status=200, response=Json.dumps(response), mimetype="application/json")
    
    @requires_account
    async def get_connections(self, user: User = None): 

        connections = self.server.connections
        connections_response = []
        for connection in connections:
            if connections[connection].device is not None:
                continue

            name = connections[connection].connection_name
            connections_response.append(name)

        return Response(status=200, response=Json.dumps(connections_response), mimetype="application/json")

    @requires_account
    async def get_extension(self, user: User = None):
        data = request.get_json()

        if "module" not in data:
            return Response(status=400, response=Json.dumps({}))

        name = data["module"]
        response = await self.server.get_extensions(name)

        status_code = response[0]
        response_data = response[1]

        if status_code == 400:
            self.server.logger.error(response_data)

        return Response(status=status_code, response=Json.dumps(response_data), mimetype="application/json")
    
    @requires_account
    async def call_function(self, user: User = None):
        data = request.get_json()

        response = await self.server.call_function(data)

        status_code = response[0]
        response_data = response[1]

        if status_code == 400:
            self.server.logger.error(str(response_data))

        return Response(status=status_code, response=Json.dumps(response_data), mimetype="application/json")
    
    @requires_account
    async def get_extension_config(self, user: User = None):
        extensions: dict[str, dict] = { }
        with open("settings/extensions.json") as file:
            json = Json.loads(file.read())
            for extension in json:
                extensions[extension] = {
                    "enabled": json[extension]["enabled"],
                    "lib": json[extension]["lib"]
                }
            
        return Response(status=200, response=Json.dumps({ "extensions": extensions }), mimetype="application/json")   
    
    @requires_account
    async def server_log(self, user: User = None):
        data = request.get_json()  

        if "lines" not in data:
            return Response(status=400, response="ERROR: Key Error (lines)")

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
    
    @requires_account
    def restart(self):
        return Response("Restarting...", 200)
    
    @requires_account
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