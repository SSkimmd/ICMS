import asyncio
import json as Json
import os
import re
import utilities
import sys
import logging
import ssl
import uuid
import pickle

import extension as Extension
from asyncio import CancelledError
from datatypes import Device, Connection, User, Callback, RequestType
from datatypes import AuthenticateRequest, GetDeviceRequest, GetExtensionRequest

from pydoc import locate


class Server:
    def __init__(self, host: str, port: int, ssl_context = None, extensions: map = None):
        self.host = host
        self.port = port

        self.connections: dict[str, Connection] = {}
        self.devices: dict[str, Device] = {}

        self.extensions: map[str, Extension.Extension] = extensions
        self.running = False
        self.ssl_context = ssl_context

        self.logger = logging.getLogger("gunicorn.error")
        self.logger.setLevel(logging.INFO)

        logformatter = utilities.NoColourFormatter()
        loghandler = logging.FileHandler("logs/log.txt", mode="a", encoding="utf8")
        streamhandler = logging.StreamHandler(sys.stdout)
        loghandler.setFormatter(logformatter)

        self.logger.addHandler(loghandler)
        self.logger.addHandler(streamhandler)

    async def close(self):
        self.running = False
        self.server.close()

    async def start(self):
        self.running = True
        self.logger.info(f'Stream Server Listening at: {self.host}:{self.port}')
        self.server = await asyncio.start_server(self.create_connection, self.host, self.port)

        await self.server.serve_forever()
    
    async def get_device(self, device_name):
        if self.devices[device_name] is not None:
            return self.devices[device_name]  
        return None

    async def get_extensions(self, extension_name):
        response = {}

        if extension_name == "all":     
            for extension in self.extensions:
                response[extension] = {}
                response[extension]["functions"] = []

                extension_object: Extension.Extension = self.extensions[extension]
                functions = extension_object.get_functions()

                for func in functions:
                    arguments = extension_object.functions[func]["arguments"]
                    response[extension]["functions"].append({
                        "function": func,
                        "arguments": arguments
                    })
        else:
            if extension_name not in self.extensions: 
                return (400, 'ERROR: Module Not Found')

            extension: Extension.Extension = self.extensions[extension_name]

            response[extension_name] = {}
            response[extension_name]["functions"] = []

            functions = extension.get_functions()

            for func in functions:
                response[extension_name]["functions"].append(func)      

        if response:
            return (200, response)
        else:
            return (400, response)

    async def call_device(self, request):
        if "device" not in request and "function" not in request and "arguments" not in request:
            return (400, "ERROR: Multiple Key Errors")
        
        device_name = request["device"]
        device = await self.get_connection(name=device_name)

        if device is None:
            return (400, "ERROR: Device Not Found")
        
        request_arguments = request["arguments"]
        request_function = request["function"]

        message = {
            "type": "POST",
            "function": request_function,
            "arguments": request_arguments
        }

        json_message = Json.dumps(message)                
        device.writer.write(json_message.encode())
        await device.writer.drain()

        return (200, f'SUCCESS: Sent Message To Device: {device_name}')

    async def call_function(self, request):
        if "module" not in request and "function" not in request and "arguments" not in request: 
            return (400, 'ERROR: Multiple Key Errors')

        if "module" not in request:
            return (400, 'ERROR: Key Error (module)')

        extension_name = request["module"]
        if extension_name not in self.extensions: 
            return (400, 'ERROR: Module Not Found')

        function_name = request["function"]
        extension: Extension.Extension = self.extensions[extension_name]
        if function_name not in extension.functions: 
            return (400, 'ERROR: Key Error (function)')

        arguments = request["arguments"]
        arguments_length = len(arguments)
        expected_length = extension.functions[function_name]['function'].__code__.co_argcount - 1

        if arguments_length != expected_length: 
            return (400, f'ERROR: Argument Error: Expected {expected_length} - Found {arguments_length}')

        try:
            #check argument types
            if(extension.functions[function_name]["arguments"]):
                args = extension.functions[function_name]["arguments"]
                for argument in arguments:
                    try:
                        arg_type = locate(args[argument])
                        arguments[argument] = arg_type(arguments[argument])
                    except:
                        return(400, f'ERROR: Argument Error: {argument} Has Incorrect Type')

            response = await extension.functions[function_name]["function"](**arguments)

            if response:
                if type(response) == str:
                    if response[0:5] == "ERROR":
                        return(400, response)
                return(200, response)
        except:
            return (400, f'ERROR: Argument Name Error')
        return (400, response)
    
    async def add_device(self, connection_name: str, device: Device):
        connection: Connection = await self.get_connection(connection_name=connection_name)

        if connection is None:
            return(400, "ERROR: Failed To Get Connection")

        self.devices[connection_name] = device
        connection.device = self.devices[connection_name]

        with open(os.getcwd() + "/settings/devices/" + connection_name + ".json", 'w') as device_config:
            config = {
                "connection_name": connection_name,
                "device_name": device.device_name,
                "device_type": device.device_type
            }
            Json.dump(config, device_config, indent=4)
        return (200, "SUCCESS: Added New Device")
    
    async def authenticate(self, request: AuthenticateRequest):
        pass

    async def get_device(self, device_name: str):
        pass

    async def on_request(self, request, connection: Connection = None):
        if request is None:
            return "ERROR: Request Failed"

        request_type: RequestType = request["type"]

        if request_type == RequestType.AUTHENTICATE:
            device_name: str = request["devicename"]
            auth_request: AuthenticateRequest = AuthenticateRequest(connection.uuid, device_name)
            await self.authenticate(auth_request)

        if request_type == RequestType.GET:
            device_name: str = request["devicename"]
            await self.get_device(device_name)

        if request_type == RequestType.POST:
            pass
                   
        return "ERROR: Failed To Proccess Request"

    async def on_recieved(self, data: bytes, connection: Connection):    
        data = data.decode()
        
        try: 
            request = Json.loads(data) 
            await self.on_request(request, connection)
        except Exception as e:
            self.logger.info(repr(e)) 


    async def on_connected(self, connection: Connection):
        connection.writer.write(connection.uuid.encode())
        await connection.writer.drain()

        data = await connection.reader.read(1024)
        if data: await self.on_recieved(data, connection)
        else: return

    async def create_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        self.logger.info(f'Connection From {format(peername)}')

        connection_id: str = uuid.uuid4()
        new_connection: Connection = Connection(connection_id, writer, reader)
        await self.on_connected(new_connection)


#create a new connection
#each connection can be a new device if the device is paired with the user
#each user has multiple devices

#device can be paired through sending packet of data which will return token
#token determines if the device is paired
#token will be used to determine if the device should be stay alive despite potentially disconnecting
#potentially add permanent tokens for each device (hardware id style)

#determine if the packet of data is of json type or needs to be manually decoded
#allow user to set their own packet types with their own ways of decoding