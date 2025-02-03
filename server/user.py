import asyncio


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
        self.endpoints: list[str] = endpoints

    def create_callback(self, function, is_persistent):
        new_callback = Callback(function, is_persistent)
        self.callbacks.append(new_callback)

class Device:
    def __init__(self, device_name, device_type):
        self.device_name: str = device_name
        self.device_type: str = device_type

class User:
    def __init__(self, username: str):
        self.username: str = username
        self.devices: dict[str, str] = {}
        
        self.pinned_extensions: list[str] = []

        self.allow_guest_connections: bool = False
        self.is_admin: bool = False

        self.roles: list[str] = []