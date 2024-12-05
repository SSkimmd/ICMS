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
    def __init__(self, extensions: map = {}, users: dict[str, Connection] = {}):
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

    async def get_extensions(self, extension_name):
        response = {}

        if extension_name == "all":     
            for extension in self.extensions:
                response[extension] = {}
                response[extension]["functions"] = []

                functions = self.extensions[extension].get_functions()

                for func in functions:
                    response[extension]["functions"].append(func)
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
        response = {}

        if device_name == "all":
            for device in self.users:
                response[device] = {}
                response[device]["functions"] = []
        else:
            if device_name not in self.users:
                return(400, "ERROR: Device Not Found")

            response[device_name] = {}
            response[device_name]["functions"] = []

        if response:
            return (200, response)
        else:
            return (400, response)

    async def process_request(self, request):
        if request is not None:
            if "type" not in request: return 'ERROR: Key Error (type)'

            #=================================== CONNECT ========================================================
            if request["type"] == "CONNECT":
                if "device-name" not in request and "id" not in request: 
                    return (400, "ERROR: Multiple Key Errors")
                
                id = request["id"]
                if id not in self.users:
                    return (400, "ERROR: User ID Mismatch")

                username = request["device-name"]
                self.users[id].user = User(username)
                return (200, f'SUCCESS: Connected With Device Name - {username}')

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
                    return (400, 'ERROR: Multiple Key Errors')

                extension_name = request["module"]
                if extension_name not in self.extensions: 
                    return (400, 'ERROR: Key Error (module)')

                function_name = request["function"]
                if function_name not in self.extensions[extension_name].functions: 
                    return (400, 'ERROR: Key Error (function)')

                arguments = request["arguments"]
                arguments_length = len(arguments)
                expected_length = self.extensions[extension_name].functions[function_name].__code__.co_argcount - 1

                if arguments_length != expected_length: 
                    return (400, f'ERROR: Argument Error: Expected {expected_length} - Found {arguments_length}')

                try:
                    response = await self.extensions[extension_name].functions[function_name](**arguments)
                except:
                    return (400, f'ERROR: Argument Name Error')
                
                if response is not None:
                    return(200, response)
                else:
                    return(400, response)
        return None

    async def update(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        print('Connection From {}'.format(peername))

        #log user
        user = Connection(len(self.users), writer, reader)
        self.users[user.id] = user

        while self.running:
            data = await reader.read(4096)
            
            if not data:
                #remove user once they stop sending and recieving data
                #this needs to only delete the current connection not user though eventually
                del self.users[user.id]
                break

            try:
                http_request = await parsers.RequestParser(data.decode()).to_request()
            except:
                http_request = None


            #tunnel request somewhere
            #find module requested
            #call function requested with arguments
            #allow user to retrieve all functions or specific module functions
            if http_request is None:
                try:
                    request = Json.loads(data.decode())
                    response = await self.process_request(request)
                    string = Json.dumps(response)
                    writer.write(string.encode())
                except:
                    continue
            else:
                print(http_request.data)
                try:
                    request_json = ''.join(http_request.data)
                    request = Json.loads(request_json)
                    request["id"] = user.id

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