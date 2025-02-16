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
        self.app.add_url_rule("/upload", view_func=self.upload_extension, methods=["POST"])

    async def download_extension(self, extension):


        pass

    async def get_extensions(self):
        
        
        pass

    async def upload_extension(self):
        file = request.files['file']
        new_path = "extensions/" + file.filename
        file.save(new_path)

        return "worked?"


def StartStoreServer():
    server = StoreServer()
    
    return server.app