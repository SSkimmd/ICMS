from adafruit_led_animation.animation.rainbow import Rainbow

class Leds:
    def __init__(self, strip):
        self.strip = strip
        self.rainbow_running = False
    
    def solid_colour(self, colour):
        self.rainbow_running = False
        print(colour)
        for i in range(240):
            self.strip[i] = colour
        self.strip.show()
        
    async def solid_colour_from_json(self, colour):
        self.rainbow_running = False
        print(colour)
        for i in range(240):
            self.strip[i] = (colour[0][0], colour[0][1], colour[0][2])
        self.strip.show()
        
    async def create_rainbow(self):
        if self.rainbow_running:
            return
        r = Rainbow(self.strip, 0.1)
        self.rainbow_running = True
        while self.rainbow_running:
            r.animate()