import neopixel
import board
import wifi
import ipaddress
import socketpool
import network
import asyncio
import leds
import time
import json

#colour = None

async def connect():
    global strip
    global controller
    global wifi_connected
    global pool
    
    ssid = ""
    password = ""
    default_leds = (5, 0, 1)
    retry_delay = 120
    enabled = False
    
    
    if not enabled:
        controller.solid_colour(default_leds)
        return

    if not wifi_connected:
        try:
            wifi.radio.connect(ssid, password)
            pool = socketpool.SocketPool(wifi.radio)
            wifi_connected = True
            print("Connected To Wifi")
        except:
            print("Could Not Connect To Wifi")
            wifi_connected = False
    
    if wifi_connected:
        net = network.Network('192.168.1.167', 8080, pool)
        net.register_endpoint(network.Endpoint("solid_colour", controller.solid_colour_from_json))
        net.register_endpoint(network.Endpoint("create_rainbow", controller.create_rainbow))


        endpoints = list(net.endpoints)
        registered = await net.register(json.dumps({
            "type": 'register',
            "username": 'leds',
            "functions": endpoints
        }))
        
        if registered is not None:
            loop = asyncio.get_event_loop()
            loop.create_task(net.recieve())
            loop.run_forever()
            
            print("Server Connection Lost")
            asyncio.run(connect())
            return
        if registered is None:
            print(f'Waiting {retry_delay} Seconds Before Re-Try')
            await asyncio.sleep(retry_delay)
            asyncio.run(connect())
            return
    else:
        controller.solid_colour(default_leds)
        
strip = neopixel.NeoPixel(board.GP2, 240)
controller = leds.Leds(strip)

wifi_connected = False
pool = None

asyncio.run(connect())
