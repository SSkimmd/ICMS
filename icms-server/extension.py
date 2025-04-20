from streamserver import Server as StreamServer
import inspect

# add more stuff here to be able to interact with the server without specifically having access to it

class Extension(object):
    def __init__(self, server: StreamServer):
        self.server: StreamServer = server
        self.functions: map[str, function] = {}

    def register_function(self, function, args = None):
        self.functions[function.__name__] = { }
        self.functions[function.__name__]["function"] = function

        if args is not None:
            self.functions[function.__name__]["arguments"] = args
        else:
            self.functions[function.__name__]["arguments"] = { }

    def unregister_function(self, name: str):
        del self.functions[name]

    def get_functions(self):
        return list(self.functions.keys())