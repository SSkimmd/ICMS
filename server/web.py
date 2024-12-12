import logging
import time
import json as Json
import sys

from app import App as Server
from threading import Thread
from flask import Flask, request
from flask import Response
from user import User
from flask_cors import CORS

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
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



@app.route("/extensions/call", methods=["POST"])
async def call_function():
    data = request.get_json()
    response = await server.stream_server.process_request(data)

    status_code = response[0]
    response_data = response[1]

    return Response(status=status_code, response=Json.dumps(response_data))



@app.route("/extensions")
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

@app.route("/server-info")
def info():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=False)