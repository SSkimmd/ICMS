import asyncio
from asyncio import CancelledError
import json as Json
import parsers as parsers
import sys
from user import *


# event system
# subscribe to an event
# ex. OnRecieved() will call all subscriptions when data is recieved
# extensions can then use this to subscribe their own callbacks

class Server:
    def __init__(self, extensions: map = { }, users: dict[str, Connection] = { }):
        self.users: dict[int, Connection] = users
        self.extensions: map = extensions
        self.running = False
        self.server = None

    def close(self):
        self.running = False
        self.server.close()

    async def start(self):
        self.server = await asyncio.start_server(self.update, '0.0.0.0', 8080)
        self.running = True

        async with self.server:
            try:
                print('Stream Server Started...')
                await self.server.serve_forever()
            except CancelledError:
                print("Server Closed")

    async def get_user(self, id = None, name = None):
        if id is not None:
            return self.users[id]
        if name is not None:
            for user in self.users:
                if self.users[user].device_name == name:
                    return self.users[user]             
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

    async def get_devices(self, device_name):
        response = { }
        if device_name == "all":
            response["devices"] = { }
            for user in self.users:
                response["devices"][self.users[user].device_name] = { "device_type": self.users[user].device_type }       
        else:
            if device_name not in self.users:
                return(400, "ERROR: Device Not Found")
            
            response["devices"] = { }
            response["devices"][device_name] = { "device_type": self.users[device_name].device_type }

        if response:
            return (200, response)
        else:
            return (400, response)

    async def process_request(self, request):
        if request is not None:
            if "type" not in request: return 'ERROR: Key Error (type)'
            #create a callback
            #when server function is called, also call all functions assigned to that trigger 
            #enables two way communication through basic event system
            #args 1:
            #(device callback): [string]      - function to be called on the device when trigger function is called
            #(server trigger):  [string]      - function which calls device function when called
            #args 2:
            #(server input callback):         - function to be called when data is recieved from the output device
            if request["type"] == "CALLBACK":
                pass
            #=================================== CONNECT ========================================================
            #args:
            #(device-name): [string]              - the name of the connected device
            #(device-type): [input][output][both] - the type of the connected device
            #
            #[input]  - only recieve data from the server to device
            #[output] - only recieve data from device to server, no specific packet structure required
            #[both]   - allow two way callbacks between device and server
            if request["type"] == "CONNECT":
                if "device-name" not in request and "id" not in request and "device-type" not in request: 
                    return (400, "ERROR: Multiple Key Errors")


                id = request["id"]
                if id not in self.users:
                    return (400, "ERROR: User ID Mismatch")


                device_name = request["device-name"]
                device_type = request["device-type"]
                self.users[id].device_name = device_name
                self.users[id].device_type = device_type

                return (200, f'SUCCESS: Connected With Device Name - {device_name}')

            #==================================== GET =======================================================           
            if request["type"] == "GET":
                if "module" not in request and "device" not in request: return

                if "module" in request:
                    response = await self.get_extensions(request["module"])
                    return response
                if "device" in request:
                    response = await self.get_devices(request["device"])
                    return response
                
            #==================================== POST =======================================================
            if request["type"] == "POST":
                if "module" not in request and "function" not in request and "arguments" not in request: 
                    print('ERROR: Multiple Key Errors')
                    return (400, 'ERROR: Multiple Key Errors')

                extension_name = request["module"]
                if extension_name not in self.extensions: 
                    print('ERROR: Key Error (module)')
                    return (400, 'ERROR: Key Error (module)')

                function_name = request["function"]
                if function_name not in self.extensions[extension_name].functions: 
                    print('ERROR: Key Error (function)')
                    return (400, 'ERROR: Key Error (function)')

                arguments = request["arguments"]
                arguments_length = len(arguments)
                expected_length = self.extensions[extension_name].functions[function_name]['function'].__code__.co_argcount - 1

                print(arguments)

                if arguments_length != expected_length: 
                    return (400, f'ERROR: Argument Error: Expected {expected_length} - Found {arguments_length}')

                try:
                    #check argument types
                    if(self.extensions[extension_name].functions[function_name]["arguments"]):
                        args = self.extensions[extension_name].functions[function_name]["arguments"]
                        for argument in arguments:
                            try:
                                if args[argument] == 'int':
                                    arguments[argument] = int(arguments[argument])
                                if args[argument] == 'bool':
                                    arguments[argument] = bool(arguments[argument])
                                if args[argument] == 'str':
                                    arguments[argument] = str(arguments[argument])
                            except:
                                return(400, f'ERROR: Argument Error: {argument} Has Incorrect Type')


                    response = await self.extensions[extension_name].functions[function_name]["function"](**arguments)
                    #also call all callbacks
                except:
                    print('ERROR: Argument Name Error')
                    return (400, f'ERROR: Argument Name Error')

                if response[0:5] == "ERROR":
                    return (400, response)

                if response is not None:
                    return (200, response)
                else:
                    return (400, response)
        return None

    async def update(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        print('Connection From {}'.format(peername))

        #log user
        user = None

        while self.running:
            data = await reader.read(4096)
            
            if not data:
                if user is not None:
                    print(f'Device Disconnected: {self.users[user.id]}')
                    del self.users[user.id]
                break

            try:
                http_request = await parsers.RequestParser(data.decode()).to_request()
            except:
                http_request = None

                # only allow socket devices to use connect packet type
                # create user
                user = Connection(len(self.users), writer, reader)
                self.users[user.id] = user



            #f request is not a HTTP request
            if http_request is None:
                try:
                    request = Json.loads(data.decode())
                    request["id"] = user.id

                    response = await self.process_request(request)
                    string = Json.dumps(response)
                    
                    writer.write(string.encode())
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