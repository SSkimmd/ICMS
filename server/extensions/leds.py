from extension import Extension
from threading import Thread
import time

class LEDS(Extension):
    def __init__(self, server):
        super().__init__(server)
        
        self.colour = 0
        self.pattern = ""
        
        self.register_function(self.change_colour, {
            "colour": "int"
        })
        self.register_function(self.change_pattern, {
            "pattern": "str"
        })

    async def change_colour(self, colour):
        self.colour = colour
        return self.colour
    
    async def change_pattern(self, pattern):
        self.pattern = pattern
        return self.pattern

def initialise(server):
    leds = LEDS(server)
    return leds