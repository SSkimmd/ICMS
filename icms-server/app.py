from webserver import WebServer
from streamserver import Server as StreamServer
from threading import Thread

def StartWebServer():
    server = WebServer()
    server_thread = Thread(target=server.start, daemon=True)
    server_thread.start()

    return server.app