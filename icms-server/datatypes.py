import asyncio
import bcrypt


class Callback:
    def __init__(self, function, is_persistent = False):
        self.function = function
        self.is_persistent = is_persistent

class Connection:
    def __init__(self, id: int, writer: asyncio.StreamWriter, reader: asyncio.StreamReader, endpoints = None):
        self.id = id
        self.writer: asyncio.StreamWriter = writer
        self.reader: asyncio.StreamReader = reader
        self.callbacks: list[Callback] = []
        self.connection_name = ""
        self.device: Device = None
        self.connected = False
        
        if endpoints is None: self.endpoints: list[str] = []
        else: self.endpoints = endpoints

    def create_callback(self, function, is_persistent):
        new_callback = Callback(function, is_persistent)
        self.callbacks.append(new_callback)

class Device:
    def __init__(self, device_name, device_type):
        self.device_name: str = device_name
        self.device_type: str = device_type

class User:
    def __init__(self, username: str, password: str, token: str = "", id: int = -1):
        self.id = id
        self.username: str = username
        
        #hashed
        self.password: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.current_token: str = token

        self.devices: dict[str, str] = {}
        
        self.pinned_extensions: list[str] = []

        self.is_admin: bool = False
        self.roles: list[str] = []