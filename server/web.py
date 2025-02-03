import logging
import time
import json as Json
import sys
import os
import ssl
import util

from app import App as Server
from threading import Thread
from flask import Flask, request
from flask import Response
from user import User, Connection, Device
from flask_cors import CORS

app = Flask(__name__)

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


@app.route("/login")
def user_login():
    pass


@app.route("/register", methods=["POST"])
def user_register():
    data = request.get_json()

    if 'username' not in data:
        return(400, 'ERROR: Key Error (username)')
    
    if 'password' not in data:
        return(400, 'ERROR: Key Error (password)')

    username = data["username"]
    user = User(username)


    return(200, f'SUCCESS: Registered {username}')

@app.route("/devices/add", methods=["POST"])
async def add_device():
    global server

    data = request.get_json()
    
    connection_name = data["connection_name"]
    name = data["device_name"]
    type = data["device_type"]

    response = await server.stream_server.add_device(connection_name, Device(name, type))

    status_code = response[0]
    response_data = response[1]

    return Response(status=status_code, response=Json.dumps({ "response": response_data }))
    #persistent device saving


@app.route("/devices", methods=["GET"])
async def get_devices():
    global server

    devices = server.stream_server.devices
    devices_response = {}
    for device in devices:
        devices_response[device] = {
            "device_name": devices[device].device_name,
            "device_type": devices[device].device_type
        }
    return Response(status=200, response=Json.dumps(devices_response))

@app.route("/device", methods=["POST"])
async def call_device():
    global server

    data = request.get_json()
    response = await server.stream_server.call_device(data)

    status_code = response[0]
    response_data = response[1]

    if status_code == 400:
        server.stream_server.logger.error(response_data)

    return Response(status=status_code, response=Json.dumps(response_data))

@app.route("/connections", methods=["GET"])
async def get_connections():
    global server

    connections = server.stream_server.connections
    connections_response = []
    for connection in connections:
        if connections[connection].device is not None:
            continue

        name = connections[connection].connection_name
        connections_response.append(name)

    return Response(status=200, response=Json.dumps(connections_response))

@app.route("/extension", methods=["POST"])
async def get_extension():
    global server

    data = request.get_json()

    if "module" not in data:
        return Response(status=400, response=Json.dumps({}))

    name = data["module"]
    response = await server.stream_server.get_extensions(name)

    status_code = response[0]
    response_data = response[1]

    if status_code == 400:
        server.stream_server.logger.error(response_data)

    return Response(status=status_code, response=Json.dumps(response_data))

@app.route("/extensions", methods=["POST"])
async def call_function():
    global server

    data = request.get_json()
    response = await server.stream_server.call_function(data)

    status_code = response[0]
    response_data = response[1]

    if status_code == 400:
        server.stream_server.logger.error(response_data)

    return Response(status=status_code, response=Json.dumps(response_data))


@app.route("/extensions", methods=["GET"])
def get_extension_config():
    global server

    extensions: dict[str, dict] = { }
    with open("settings/extensions.json") as file:
        json = Json.loads(file.read())
        for extension in json["extensions"]:
            name = list(extension.keys())[0]
            extensions[name] = {
                "enabled": extension[name]["enabled"],
                "lib": extension[name]["lib"] 
            }
        
    return Response(
    response=Json.dumps({
        "extensions": extensions
    }), 
    status=200, 
    mimetype='application/json')    



@app.route("/serverlog", methods=["POST"])
def server_log():
    global server

    data = request.get_json()
    lines = int(data["lines"])
    out = ""


    log = util.reverse_readline("logs/log.txt")

    count = 0
    for line in log:
        if count == lines:
            break

        if line[0:2] == "  ":
            continue

        out += line + "\n"
        count += 1


    return Response(
        response=out, 
        status=200, 
        mimetype='application/json'
    )                


@app.route("/server-info")
def server_info():
    global server
    global server_thread

    uptime = time.time() - start_time

    return Response(
    response=Json.dumps({
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


def run_flask(should_return = True):
    global server
    global server_thread
    global start_time

    log = logging.getLogger('gunicorn.error')
    #sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #sslcontext.load_cert_chain('certificates/cert.pem', keyfile='certificates/key.pem')
    #sslcontext.verify_mode = ssl.VerifyMode.CERT_REQUIRED
    #sslcontext.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')

    CORS(app, resources={
        "/*": {
            "origins": "*"
        }
    })

    server = Server()
    server.init_extensions()

    server_thread = Thread(target=server.start, daemon=True)
    server_thread.start()
    start_time = time.time()

    if should_return:
        return app

if __name__ == "__main__":
    run_flask(False)