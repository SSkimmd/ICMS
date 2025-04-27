import asyncio
import logging
import time
import json as Json
import sys
import os
import ssl
import datetime

import jwt.api_jwt
import utilities
import importlib
import jwt
import bcrypt

from functools import wraps
from extension import Extension
from threading import Thread
from flask import Flask, request
from flask import Response
from datatypes import Device, Connection, User
from flask_cors import CORS
from streamserver import Server as StreamServer
from database import db_create_user, db_get_user_by_username, db_get_user_by_id, db_get_users, db_create_database



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

        self.logger = logging.getLogger("gunicorn.error")

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

    def check_files(self):
        if not os.path.isfile("./settings/extensions.json"):
            with open("./settings/extensions.json", 'w') as file:
                Json.dump({}, file, indent=4)
            self.logger.error("ERROR: Could Not Find File /settings/extensions.json, Created New File Instead")

        if not os.path.isfile("./settings/server.json"):
            with open("./settings/extensions.json", 'w') as file:
                Json.dump({}, file, indent=4)
            self.logger.error("ERROR: Could Not Find File /settings/server.json, Created New File Instead")

        if not os.path.isfile("./logs/log.txt"):
            file = open("./logs/log.txt", 'x')

    def init_users(self):
        with open("./settings/server.json", 'r') as file:
            json = Json.load(file)
            started = json["started"]

            if started:
                self.users: list[User] = asyncio.run(db_get_users())
                for user in self.users:
                    self.logger.info(f'Loaded User: {user.username}')
            else:
                try:
                    self.logger.info("INFO: Application Is Being Run For The First Time")
                    asyncio.run(db_create_database())
                    json["started"] = True
                except Exception as e:
                    self.logger.error(f'ERROR: {repr(e)}')
                    self.logger.info("INFO: Try Deleting The database.db File And Restarting")

        if json is None:
            return None
        
        if not started:
            with open("./settings/server.json", 'w') as file:
                self.logger.info("INFO: First Start Complete")
                Json.dump(json, file, indent=4)

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
                        self.logger.info(f'Reimporting: {extension}')
                    new_module = importlib.import_module(lib) 
                    new_extension: Extension = new_module.initialise(self.server)
                    self.extensions[extension] = new_extension
                    self.logger.info(f'Started Extension: {extension}')
                except:
                    self.logger.info(f'Failed To Import Module Name: {extension}')
                    continue
        return
    
    def requires_account(f):
        @wraps(f)
        async def decorated(self, *args, **kwargs):
            token = request.headers.get("Authorization", None)

            if token is None:
                return Response(status=400, response="ERROR: Authorization Header Not Found")

            user_id = await get_user_id(token)
            user: User = await self.get_user_with_id(user_id=user_id)

            if user is None:
                return Response(status=400, response="ERROR: User Not Found")

            if token != user.current_token:
                return Response(status=400, response="ERROR: Incorrect Token")

            return await f(self, *args, user, **kwargs)
        return decorated    

    async def get_user_with_credentials(self, credentials):
        if "username" not in credentials or "password" not in credentials:
            return None
        
        password: bytes = credentials["password"]
        username: str = credentials["username"]

        for user in self.users:
            if user is None: continue

            if user.username == credentials["username"]:
                if bcrypt.checkpw(password, user.password.encode('utf-8')):
                    self.logger.info(f'INFO: Retrieved User From Cache: Users {len(self.users)}')
                    return user

        user: User = await db_get_user_by_username(username)

        if user is None:
            return None

        if bcrypt.checkpw(password, user.password.encode('utf-8')):
            self.users.append(user)
            self.logger.info(f'INFO: Retrieved User From Database: Users {len(self.users)}')
            return user
        
        return None
        
    async def get_user_with_id(self, user_id: int):
        for user in self.users:
            if user.id == user_id:
                return user
            
        user: User = await db_get_user_by_id(user_id)
        return user
        
    async def create_new_user(self, user: User):
        password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode()
        user.password = password

        try:
            await db_create_user(user)
            self.logger.info("SUCCESS: Created New User")
        except Exception as e:
            self.logger.error(repr(e))
            return False
        return True

    async def user_login(self):
        """
            Make This Look Nicer
        """

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

        user: User = await self.get_user_with_credentials(credentials=credentials)

        if user is None:
            return Response(status=400, response="ERROR: User Not Found (Login)")

        try:
            decoded = jwt.api_jwt.decode(user.current_token, "secret", algorithms=["HS256"])
        except:
            self.logger.error("ERROR: Incorrect Token Supplied (Login)")
            return Response(status=400, response="ERROR: Incorrect Token Supplied")

        if user is None:
            return Response(status=400, response="ERROR: User Not Found")
        
        self.logger.info(f'SUCCESS: User Logged In: {user.username}')
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

        user: User = User(username, password, token=user_token, id=user_id)

        created = None
        try:
            created = await self.create_new_user(user)
        except Exception as e:
            print(repr(e))

        if created is None:
            return Response(status=400, response="ERROR: Failed To Create User")

        self.users.append(user)

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
        log = utilities.reverse_readline("logs/log.txt")
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
    
    def get_settings(self):
        with open("./settings/server.json") as file:
            server_settings = Json.load(file)

        if server_settings is None:
            return

        server_host = server_settings["servers"]["host"]
        server_port = server_settings["servers"]["stream"]["port"]

        return server_host, server_port

    def start(self):
        self.check_files()
        self.init_users()
        self.init_extensions()

        server_host, server_port = self.get_settings()

        self.server = StreamServer(host=server_host, port=server_port)
        self.server.extensions = self.extensions
        self.server.users = self.users

        self.start_time = time.time()
        asyncio.run(self.server.start())

        return Response("Starting...", 200)