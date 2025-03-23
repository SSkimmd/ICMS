import asyncio
import logging
import time
import json as Json
import sys
import os
import ssl
import importlib
import sqlite3

from threading import Thread
from flask import Flask, request
from flask import Response
from flask_cors import CORS

class StoreServer:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.add_url_rule("/extensions/<extension>", view_func=self.download_extension, methods=["GET"])
        self.app.add_url_rule("/extensions/upload", view_func=self.upload_extension, methods=["POST"])
        self.app.add_url_rule("/extensions", view_func=self.get_extensions, methods=["GET"])

        self.app.add_url_rule("/devices/<device>", view_func=self.download_device, methods=["GET"])
        self.app.add_url_rule("/devices/upload", view_func=self.upload_device, methods=["POST"])
        self.app.add_url_rule("/devices", view_func=self.get_devices, methods=["GET"])


    async def download_device(self, device):
        pass

    async def upload_device(self):
        pass

    async def get_devices(self):
        devices = { }
        for name in os.listdir("devices"):
            with open("devices/" + name + "/device.json") as file:
                device = Json.loads(file.read())
                devices[name] = device 
        return devices

    async def download_extension(self, extension):
        pass

    async def get_extensions(self):
        extensions = { }
        for name in os.listdir("extensions"):
            with open("extensions/" + name + "/extension.json") as file:
                extension = Json.loads(file.read())
                extensions[name] = extension 
        return extensions

    async def upload_extension(self):
        file = request.files['file']
        new_path = "extensions/" + file.filename
        file.save(new_path)

        return ""


def StartStoreServer():
    server = StoreServer()
    
    return server.app