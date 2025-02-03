import asyncio
import json as Json
import os
import re
import util
import sys
import logging
import ssl

from asyncio import CancelledError
from user import *
from pydoc import locate

class Server:
    def __init__(self, ssl_context = None, extensions: map = { }):
        self.connections: dict[int, Connection] = {}
        self.devices: dict[str, Device] = {}

        self.extensions: map = extensions
        self.running = False
        self.server = None
        self.ssl_context = ssl_context

        self.logger = logging.getLogger("gunicorn.error")
        self.logger.setLevel(logging.INFO)

        logformatter = util.NoColourFormatter()
        loghandler = logging.FileHandler("logs/log.txt", mode="a", encoding="utf8")
        streamhandler = logging.StreamHandler(sys.stdout)
        loghandler.setFormatter(logformatter)

        self.logger.addHandler(loghandler)
        self.logger.addHandler(streamhandler)

    def close(self):
        self.running = False
        self.server.close()

    async def start(self):
        if self.ssl_context is not None:
            self.server = await asyncio.start_server(self.update, '0.0.0.0', 8080, ssl=self.ssl_context)
        else:
            self.server = await asyncio.start_server(self.update, '0.0.0.0', 8080)

        self.running = True

        async with self.server:
            self.logger.info(f'Stream Server Listening at: 0.0.0.0:8080')
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

                functions = self.extensions[extension].get_functions()

                for func in functions:
                    arguments = self.extensions[extension].functions[func]["arguments"]
                    response[extension]["functions"].append({
                        "function": func,
                        "arguments": arguments
                    })
        else:
            if extension_name not in self.extensions: 
                return (400, 'ERROR: Module Not Found')

            extension = self.extensions[extension_name]

            response[extension_name] = {}
            response[extension_name]["functions"] = []

            functions = self.extensions[extension_name].get_functions()

            for func in functions:
                response[extension_name]["functions"].append(func)      

        if response:
            return (200, response)
        else:
            return (400, response)


    async def call_device(self, request):
        if "device" not in request and "message" not in request:
            return (400, "ERROR: Multiple Key Errors")
        
        device_name = request["device"]
        device = await self.get_connection(name=device_name)

        if device is None:
            return (400, "ERROR: Device Not Found")

        message = {
            "type": "POST",
            "function": "solid_colour",
            "arguments": request['message']
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
        if function_name not in self.extensions[extension_name].functions: 
            return (400, 'ERROR: Key Error (function)')

        arguments = request["arguments"]
        arguments_length = len(arguments)
        expected_length = self.extensions[extension_name].functions[function_name]['function'].__code__.co_argcount - 1

        if arguments_length != expected_length: 
            return (400, f'ERROR: Argument Error: Expected {expected_length} - Found {arguments_length}')

        try:
            #check argument types
            if(self.extensions[extension_name].functions[function_name]["arguments"]):
                args = self.extensions[extension_name].functions[function_name]["arguments"]
                for argument in arguments:
                    try:
                        arg_type = locate(args[argument])
                        arguments[argument] = arg_type(arguments[argument])
                    except:
                        return(400, f'ERROR: Argument Error: {argument} Has Incorrect Type')


            response = await self.extensions[extension_name].functions[function_name]["function"](**arguments)

            if response:
                if type(response) == str:
                    if response[0:5] == "ERROR":
                        return(400, response)
                return(200, response)
        except:
            return (400, f'ERROR: Argument Name Error')
        return (400, response)
    
    async def add_device(self, connection_name: str, device: Device):
        self.devices[connection_name] = device
        connection: Connection = await self.get_connection(connection_name=connection_name)
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
                if "extension" in request:
                    response = await self.get_extensions(request["extension"])
                    return response
                
                return (400, "ERROR: Key Error In GET Request")
            #==================================== POST =======================================================
            if request["type"] == "POST":
                response = await self.call_function(request)
                return response
                   
        return None

    async def update(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        self.logger.info('Connection From {}'.format(peername))

        #log user
        connection = None

        while self.running:
            data = await reader.read(4096)

            if connection is not None:
                if(len(connection.callbacks) > 0):
                    for callback in connection.callbacks:
                        await callback.function(data)

                        if not callback.is_persistent:
                            connection.callbacks.remove(callback)

            if not data:
                if connection is not None:
                    self.logger.info(f'Device Disconnected: {self.connections[connection.id].device.device_name}')
                    del self.connections[connection.id]
                break

            http_request = None
            try:
                http_request = await util.RequestParser(data.decode()).to_request()
            except:
                if connection is not None: 
                    continue

                connection = Connection(len(self.connections), writer, reader)
                self.connections[connection.id] = connection



            #f request is not a HTTP request
            if http_request is None:
                try:
                    request = Json.loads(data.decode())    

                    response = await self.process_request(request, connection)

                    string = Json.dumps(response) 
                    writer.write(string.encode())
                    await writer.drain()
                except:
                    continue
            #If request is a HTTP request
            else:
                try:
                    request_json = ''.join(http_request.data)
                    request = Json.loads(request_json)

                    response = await self.process_request(request)
                    response_json = Json.dumps(response[1])

                    return_code = 'OK' if response[0] == 200 else 'Bad Request'

                    string = f'HTTP/1.1 {str(response[0])} {return_code}\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(response_json)}\r\n\n{response_json}'

                    writer.write(string.encode())
                    await writer.drain()
                except:
                    json = Json.dumps({})
                    string = f'HTTP/1.1 400 Bad Request\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(json)}\r\n\n{json}'
                    writer.write(string.encode())
                    await writer.drain()

if __name__ == "__main__":
    server = Server()
    asyncio.run(server.start())