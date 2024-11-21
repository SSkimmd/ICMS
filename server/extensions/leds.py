from extension import Extension
from threading import Thread
import time

class LEDS(Extension):
    def __init__(self, server):
        super().__init__(server)
        
        self.colour = 0
        self.register_function(self.change_colour)

    async def change_colour(self, colour):
        self.colour = colour
        return self.colour

def initialise(server):
    leds = LEDS(server)
    return leds