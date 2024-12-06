import json
import asyncio
import socketpool

class Endpoint:
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback
        


class Network:
    def __init__(self, host, port, pool):
        self.host = host
        self.port = port
        self.endpoints = {}
        self.socket = None
        self.pool = pool
        self.running = False
            
    def register_endpoint(self, endpoint):
        self.endpoints[endpoint.name] = endpoint.callback
    
    def call_endpoint(self, packet):
        if 'type' not in packet:
            return
        
        name = packet['type']
        if name in self.endpoints:
            del packet['type']
            
            args = []
            for key in packet:
                args.append(packet[key])
                
            if len(args) > 0:
                asyncio.create_task(self.endpoints[name](args))
            else:
                asyncio.create_task(self.endpoints[name]())
                
        
    async def recieve(self):            
        buffer = bytearray(256)
        self.socket.setblocking(False)
        print("Recieving...")
        while True:
            try:
                size = self.socket.recv_into(buffer)
                data = buffer.decode()
                
                if(size == 0):
                    print("Socket Error, Unable To Find Server")
                    break
                
                try:
                    packet = json.loads(data)
                    self.call_endpoint(packet)
                except:
                    await asyncio.sleep(0)
            except:
                await asyncio.sleep(0)
        return
                
    async def register(self, json_string: str):
        try:
            self.socket = self.pool.socket(self.pool.AF_INET, self.pool.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(10)
        except:
            return None
        
        data = json_string.encode()
            
        if self.socket is not None:
            size = self.socket.send(data)
            buffer = bytearray(256)
            
            try:
                self.socket.recv_into(buffer)  
                packet = buffer.decode()
                return packet
            except:
                return None
                
        
    async def send(self, json: str):
        data = json.encode()
            
        if self.socket is not None:
            try:
                size = self.socket.send(data)                    
            except:
                return
            
            
                    
                    
                    