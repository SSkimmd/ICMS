import asyncio
import bcrypt
from enum import Enum


class RequestType(Enum):
    AUTHENTICATE = 0
    POST = 1
    GET = 2

class DeviceRequest:
    """
        Base Device Request Class
    """
    def __init__(self, request_type: int):
        self.request_type: int = request_type

class AuthenticateRequest(DeviceRequest):
    """
        Device Authentication Request
    """
    def __init__(self, connection_id: str, device_name: str):
        super.__init__(0)
        self.connection_id: str = connection_id
        self.device_name: str = device_name

class DevicePostRequest(DeviceRequest):
    """
        Device Post Request
    """
    def __init__(self, )









class Callback:
    def __init__(self, function, is_persistent = False):
        self.function = function
        self.is_persistent = is_persistent

class Connection:
    def __init__(self, uuid: str, writer: asyncio.StreamWriter, reader: asyncio.StreamReader, endpoints = None):
        self.uuid: str = uuid
        self.writer: asyncio.StreamWriter = writer
        self.reader: asyncio.StreamReader = reader
        self.device: Device = None


class Device:
    def __init__(self, device_name, device_type):
        self.device_name: str = device_name
        self.device_type: str = device_type

class User:
    def __init__(self, username: str, password: str, token: str = "", id: int = -1):
        self.id = id
        self.username: str = username
        
        #hashed
        self.password: str = password
        self.current_token: str = token

        self.devices: dict[str, str] = {}
        
        self.pinned_extensions: list[str] = []

        self.is_admin: bool = False
        self.roles: list[str] = []