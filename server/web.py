import logging
import time
import json as Json
import sys
import os
import ssl

from app import App as Server
from threading import Thread
from flask import Flask, request
from flask import Response
from user import User
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



@app.route("/extensions/call", methods=["POST"])
async def call_function():
    global server

    data = request.get_json()
    response = await server.stream_server.process_request(data)

    status_code = response[0]
    response_data = response[1]

    if status_code == 400:
        server.stream_server.logger.error(response_data)

    return Response(status=status_code, response=Json.dumps(response_data))


@app.route("/extensions", methods=["POST", "GET"])
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

def reverse_readline(filename, buf_size=8192):
    """A generator that returns the lines of a file in reverse order"""
    with open(filename, 'rb') as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            # remove file's last "\n" if it exists, only for the first buffer
            if remaining_size == file_size and buffer[-1] == ord('\n'):
                buffer = buffer[:-1]
            remaining_size -= buf_size
            lines = buffer.split('\n'.encode())
            # append last chunk's segment to this chunk's last line
            if segment is not None:
                lines[-1] += segment
            segment = lines[0]
            lines = lines[1:]
            # yield lines in this chunk except the segment
            for line in reversed(lines):
                # only decode on a parsed line, to avoid utf-8 decode error
                yield line.decode()
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment.decode()



@app.route("/server-log", methods=["POST"])
def server_log():
    global server

    data = request.get_json()
    lines = int(data["lines"])
    out = ""


    log = reverse_readline("log.txt")

    count = 0
    for line in log:
        if count == lines:
            break

        out += line
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


def run_flask():
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

    return app

if __name__ == "__main__":
    run_flask()