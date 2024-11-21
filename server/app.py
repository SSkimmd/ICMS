import json as Json
import importlib
import asyncio
import threading
from stream import Server as StreamServer
from user import User


class App:
    def __init__(self):
        self.extensions: map = {}
        self.stream_server: StreamServer = StreamServer()

    #ensure these actually return errors at somepoint instead of just breaking
    def init_extensions(self):
        with open("./settings/extensions.json") as file:
            json = Json.loads(file.read())

            if not "extensions" in json: return

            for extension in json["extensions"]:
                name = list(extension.keys())[0]

                if not "lib" in extension[name] or not "enabled" in extension[name]: break
                if not extension[name]["enabled"]: break

                lib = extension[name]["lib"]

                try:
                    new_module = importlib.import_module(lib)  
                    new_extension = new_module.initialise(self.stream_server)
                    self.extensions[name] = new_extension
                    print(f'Started Extension: {name}')
                except:
                    print(f'Failed To Import Module Name: {name}')
                    continue
        return

    def start(self):
        self.stream_server.extensions = self.extensions
        asyncio.run(self.stream_server.start())

if __name__ == "__main__":
    app = App()
    app.init_extensions()
    app.start()