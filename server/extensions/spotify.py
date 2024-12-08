from extension import Extension
from threading import Thread
import asyncio
import time
import json as Json


class Spotify(Extension):
    def __init__(self, server):
        super().__init__(server)
        
        self.volume = 0
        self.register_function(self.change_volume, {
            "volume": "int"
        })
        
    async def change_volume(self, volume):
        self.volume = volume
        return self.volume


def initialise(server):
    spotify = Spotify(server)
    return spotify