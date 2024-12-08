from app import App as Server
from threading import Thread

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import time
from flask import Flask
from flask import Response

import json as JSON
import sys

app = Flask(__name__)
server = Server()
server.init_extensions()

server_thread = Thread(target=server.start, daemon=True)
server_thread.start()
start_time = time.time()


def start_server():
    global server
    global server_thread  
    global start_time  

    #for extension in server.extensions:

    server.stream_server.close()

    server = None
    server_thread = None

    server = Server()
    server.init_extensions()
    server_thread = Thread(target=server.start, daemon=True)
    server_thread.start()

    start_time = time.time()

@app.route("/server-info")
def info():
    global server
    global server_thread

    uptime = time.time() - start_time

    return Response(
    response=JSON.dumps({
        "server_running": server.stream_server.running,
        "server_uptime": round(uptime, 2)
    }), 
    status=200, 
    mimetype='application/json')

@app.route("/restart")
def restart():
    start_server()
    return Response("Restarting...", 200)

@app.route("/start")
def start():
    start_server()
    return Response("Starting...", 200)


@app.route("/stop")
def stop():
    global server
    global server_thread
    global start_time

    server.stream_server.close()
    return Response("Stopping...", 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)