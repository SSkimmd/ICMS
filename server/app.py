import json as Json
import importlib
import asyncio
import threading
import sys
from stream import Server as StreamServer


class App:
    def __init__(self, ssl_context = None):
        self.extensions: map = {}
        self.stream_server: StreamServer = StreamServer(ssl_context=ssl_context)

    #ensure these actually return errors at somepoint instead of just breaking
    def init_extensions(self):
        with open("./settings/extensions.json") as file:
            json = Json.loads(file.read())

            if not "extensions" in json: return

            for extension in json["extensions"]:
                name = list(extension.keys())[0]

                if "lib" not in extension[name] or "enabled" not in extension[name]: 
                    print("ERROR: Extension Multiple Key Error")
                    continue
                
                if not extension[name]["enabled"]:
                    print(f'Skipping Extension: {name}')
                    continue

                lib = extension[name]["lib"]

                try:
                    if sys.modules.get(lib):
                        sys.modules.pop(lib)
                        print(f'Reimporting: {name}')
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

        try:
            asyncio.run(self.stream_server.start())
        except:
            pass

if __name__ == "__main__":
    app = App()
    app.init_extensions()
    app.start()