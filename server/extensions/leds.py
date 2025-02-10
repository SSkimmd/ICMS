from extension import Extension
from threading import Thread
import asyncio
import time
import json as Json
from datatypes import Connection
from stream import Server as StreamServer

class LEDS(Extension):
    def __init__(self, server: StreamServer):
        super().__init__(server)
        
        self.colour = 0
        self.pattern = ""
        self.devices: dict[str, Connection] = { }
        
        self.register_function(self.change_colour, {
            "device_name": "str",
            "r": "int",
            "g": "int",
            "b": "int"
        })
        self.register_function(self.change_pattern, {
            "pattern": "str"
        })
        self.register_function(self.connect, {
            "device_name": "str"
        })
        self.register_function(self.test)


    async def device_callback(self, data):
        print(f'callback called, data: {data}')

    async def test(self):
        return "SUCCESS: Test Success"

    async def change_colour(self, device_name: str, r: int, g: int, b: int):
        if device_name not in self.devices:
            return "ERROR: Device Does Not Exist"

        response = {
            "type": "POST",
            "function": "solid_colour",
            "arguments": {
                "r": r,
                "g": g,
                "b": b
            }
        }
        
        self.devices[device_name].writer.write(Json.dumps(response).encode())
        self.devices[device_name].writer.drain()
        return "SUCCESS: Set Colour"
    
    async def change_pattern(self, pattern):
        self.pattern = pattern
        return self.pattern
    
    # connect led controller
    async def connect(self, device_name):
        device = await self.server.get_connection(name=device_name)

        if device is None: return "ERROR: Device Doesn't Exist"
        
        self.devices[device_name] = device

def initialise(server) -> Extension:
    leds = LEDS(server)
    return leds