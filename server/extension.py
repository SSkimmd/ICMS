from stream import Server as StreamServer
import inspect

class Extension(object):
    def __init__(self, server):
        self.server: StreamServer = server
        self.functions: map = {}

    def read_callback(self, callback):
        pass

    def register_function(self, function):
        self.functions[function.__name__] = function

    def unregister_function(self, name: str):
        self.functions.pop(name, None)

    def get_functions(self):
        return list(self.functions.keys())