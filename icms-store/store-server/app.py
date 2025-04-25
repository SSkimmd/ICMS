import asyncio
import logging
import time
import json as Json
import sys
import os
import ssl
import importlib
import aiosqlite

from threading import Thread
from flask import Flask, request, send_file
from flask import Response
from flask_cors import CORS
from werkzeug.utils import secure_filename



#==================================================== MAKE THE AUTH SERVER AND SWITCH THIS SHIT TO A SQLITE DATABASE YOU DUMB FUCK







class StoreServer:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.add_url_rule("/extensions/<extension>", view_func=self.download_extension, methods=["GET"])
        self.app.add_url_rule("/extensions/upload", view_func=self.upload_extension, methods=["POST"])
        self.app.add_url_rule("/extensions", view_func=self.get_extensions, methods=["GET"])

        self.app.add_url_rule("/devices/<device>", view_func=self.download_device, methods=["GET"])
        self.app.add_url_rule("/devices/upload", view_func=self.upload_device, methods=["POST"])
        self.app.add_url_rule("/devices", view_func=self.get_devices, methods=["GET"])

        self.app.add_url_rule("/test", view_func=self.db_test, methods=["GET"])  
    
    async def db_test(self):
        try:
            async with aiosqlite.connect('database.db') as db:
                #table = """
                #CREATE TABLE devices (
                #    id INTEGER PRIMARY KEY,
                #    name TEXT NOT NULL,
                #    type TEXT NOT NULL,
                #    date INTEGER NOT NULL
                #); 
                #"""
                #await db.execute(table)
                #await db.execute("INSERT INTO devices (name, type, date) VALUES ('RPI Pico-W', '', 1)")
                #await db.commit()
                return Response(status=200, response={})
        except Exception as e:
            print(repr(e))
            return Response(status=400, response='failed')



    async def download_device(self, device):
        print("downloading device " + device)
        name = secure_filename(device)
        file = os.path.join('devices/', name + ".zip")
        return send_file(file, as_attachment=True)
        
    async def upload_device(self):
        pass

    async def get_devices(self):
        devices = { }
        for name in os.listdir("devices"):
            path = os.path.abspath(os.getcwd() + "/devices")
            dir = os.path.join(path, name)
            if os.path.isdir(dir):
                with open("devices/" + name + "/device.json") as file:
                    device = Json.loads(file.read())
                    devices[name] = device 
        return devices

    async def download_extension(self, extension):
        print("downloading extension " + extension)
        name = secure_filename(extension)
        file = os.path.join('extensions/', name + ".zip")
        return send_file(file, as_attachment=True)

    async def get_extensions(self):
        extensions = { }
        for name in os.listdir("extensions"):
            path = os.path.abspath(os.getcwd() + "/extensions")
            dir = os.path.join(path, name)
            if os.path.isdir(dir):
                with open("extensions/" + name + "/extension.json") as file:
                    extension = Json.loads(file.read())
                    extensions[name] = extension 
        return extensions

    async def upload_extension(self):
        print(request.form)
        file = request.files['file']
        new_path = request.form['type'] + "s/" + request.form['name'] + ".zip"
        file.save(new_path)

        return "worked"


def StartStoreServer():
    server = StoreServer()
    
    return server.app