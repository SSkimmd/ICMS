import asyncio
import json as Json
import os
import re
import util
import sys
import logging
import ssl
import extension as Extension

from asyncio import CancelledError
from datatypes import Device, Connection, User, Callback
from pydoc import locate


class Server:
    def __init__(self, ssl_context = None, extensions: map = None):
        self.connections: dict[int, Connection] = {}
        self.devices: dict[str, Device] = {}

        self.extensions: map[str, Extension.Extension] = extensions
        self.running = False
        self.ssl_context = ssl_context

        self.logger = logging.getLogger("gunicorn.error")
        self.logger.setLevel(logging.INFO)

        logformatter = util.NoColourFormatter()
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
        self.logger.info(f'Stream Server Listening at: 0.0.0.0:8080')
        self.server = await asyncio.start_server(self.update, '0.0.0.0', 8080)

        await self.server.serve_forever()

    async def get_connection(self, id = None, name = None, connection_name = None):
        if id is not None:
            if self.connections[id] is not None:
                return self.connections[id]       
            
        if name is not None:
            for id in self.connections:
                if self.connections[id].device.device_name == name:
                    return self.connections[id]
                
        if connection_name is not None:
            for id in self.connections:
                if self.connections[id].connection_name == connection_name:
                    return self.connections[id]

        return None
    
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

        extension_name = request["module"]
        if extension_name not in self.extensions: 
            return (400, 'ERROR: Key Error (module)')

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
    
    async def process_request(self, request, connection: Connection = None):
        """
            Proccess and perform request based on the type attribute

            Request Types

            LOG: Log-out the message contained in the request, this is used by connected devices

            POST: Similarly to the REST keyword, call a function with arguments

            GET: Also similar to the REST keyword, get data from a function or endpoint

            CONNECT: Used by client devices to connect to authenticate with the stream server
        """

        if request is not None:
            #check if user is authorised
            #if connection is None: 
            #    self.logger.error('ERROR: Connection Error')
            #    return 'ERROR: Connection Error'

            if "type" not in request: 
                return 'ERROR: Key Error (type)'
            
            #log to server logger from connected client
            #should be pre-authorised unless guest logging is enabled
            if request["type"] == "LOG":
                pass

            if request["type"] == "CONNECT":
                #login for device per new session
                if "name" not in request:
                    return (400, f'ERROR: Connection Name Key Error')
                
                if not connection:
                    return (400, f'ERROR: Connection Does Not Exist')
                
                name = request["name"]
                endpoints = request["endpoints"]
                
                connection.connection_name = name
                connection.endpoints = endpoints

                file_name = os.getcwd() + "/settings/devices/"+ name + ".json"

                if os.path.exists(file_name):
                    with open(file_name) as f:
                        config = Json.load(f)

                        if "device_name" not in config and "device_type" not in config:
                            return (200, f'ERROR: Device Config Key Error: ' + name)
                        
                        device_name = config["device_name"]
                        device_type = config["device_type"]

                        connection.device = Device(device_name, device_type)
                        self.devices[name] = connection.device
                    return (200, f'SUCCESS: Connected Existing Device: ' + name)
                return (200, f'SUCCESS: Connected New Device: ' + name)

            #==================================== GET =======================================================           
            if request["type"] == "GET":
                if "extension" not in request:
                    return (400, "ERROR: Key Error In GET Request")
                    
                response = await self.get_extensions(request["extension"])
                return response
            #==================================== POST =======================================================
            if request["type"] == "POST":
                response = await self.call_function(request)
                return response
                   
        return "ERROR: Failed To Proccess Request"

    async def update(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        self.logger.info('Connection From {}'.format(peername))

        #log user
        connection: Connection = Connection(len(self.connections), writer, reader)
        self.connections[connection.id] = connection
        connection.connected = True

        while connection.connected:
            data = await reader.read(1024)

            if not data:
                if connection is not None:
                    self.logger.info(f'Device Disconnected: {self.connections[connection.id].device.device_name}')
                    connection.connected = False
                    del self.connections[connection.id]
                break

            if connection is not None:
                if(len(connection.callbacks) > 0):
                    for callback in connection.callbacks:
                        await callback.function(data)

                        if not callback.is_persistent:
                            connection.callbacks.remove(callback)

            try:
                request = Json.loads(data.decode())
                response = await self.process_request(request, connection)
                writer.write(Json.dumps(response).encode())
                await writer.drain()
            except Exception as e:
                self.logger.info(repr(e))