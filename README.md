# ICMS
ICMS Is a set of applications used to build and debug IoT devices.
# Installation
There are two ways of installing and using ICMS.
### Docker
A Docker-Compose file can be found in the root directory of the application.\
Using the following commands the application can be built and run using the docker desktop app:
```
docker compose build
docker compose up
```
### Manual
Installation on a windows system will by default require the usage of WSL - [Get WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
### When In The /icms-app Directory
Run The Command:
```powershell
npm run host
```
### When In The /icms-server Directory
Run The Command:
```bash
./run.sh
```

# Using The WebApp
### Dashboard
The dashboard is where you will find all the important information about the server.
# Using The Server
### Connecting A New Device
New devices can be easily paired through the WebApp when the device is listed in the available connections\
Another way to connect a device is by using an account previously created and authenticating directly using the device.
### Authenticate Using A Device
At the most basic level an authenticate request is being sent to the server\
This requests consists of the follow JSON data:
```json
{
  "type": "AUTHENTICATE",
  "username": "exampleUsername",
  "password": "examplePassword",
  "device": "exampleDeviceName",
  "devicetype": "both"
}
```
### Sending A Request
There are a couple of different types of requests available:
```json
{
  "type": "GET",
  "GET": {
    "type": "DEVICE",
    "device": "exampleDeviceName"
  }
}
```
```json
{
  "type": "POST",
  "POST": {
    "type": "EXTENSION",
    "request": {
      "module": "exampleExtension",
      "function": "cool_function",
      "arguments": {
        "coolness": 999
      }
    }
  }
}
```
# Extensions
### Installing An Extension
Installing an extension is as simple as placing the folder extracted from the file and updating the extensions.json file found in /settings
```json
{
  "exampleExtension": {
    "lib": "exampleExtension.entrypoint",
    "enabled": true
  }
}
```
### Extension Functions
When creating an extension it is important to register functions with the server in order for them to become usable\
The Extension class has built in support for this using the following code:
```python
class exampleExtension(Extension):
  def __init__(self, server):
    super.__init__(server)
    self.register(cool_function)

  async def cool_function(self):
    print('this function isnt cool')
```
An added benefit of creating functions this way is being able to specify function arguments with types:
```python
class exampleExtension(Extension):
  def __init__(self, server):
    super.__init__(server)
    self.register(cool_function, {
      "coolness": "int"
    })

  async def cool_function(self, coolness: int):
    print(f'this function is this cool: {coolness}')
```









