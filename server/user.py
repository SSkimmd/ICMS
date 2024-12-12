import asyncio

class Connection:
    def __init__(self, id: int, writer: asyncio.StreamWriter, reader: asyncio.StreamReader, device_name = None, device_type = None):
        self.id = id
        self.writer: asyncio.StreamWriter = writer
        self.reader: asyncio.StreamReader = reader
        self.device_name = device_name
        self.device_type = device_type
        self.role: str = ""

class User:
    def __init__(self, username: str):
        self.username: str = username
        self.devices: dict[str, str] = {}
        
        self.pinned_extensions: list[str] = []

        self.allow_guest_connections: bool = False
        self.is_admin: bool = False

        self.roles: list[str] = []