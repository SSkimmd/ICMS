import asyncio

class User:
    def __init__(self, username: str):
        self.username = username

class Connection:
    def __init__(self, id: int, writer: asyncio.StreamWriter, reader: asyncio.StreamReader):
        self.id = id
        self.writer: asyncio.StreamWriter = writer
        self.reader: asyncio.StreamReader = reader