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
```
npm run host
```
### When In The /icms-server Directory
Run The Command:
```
./run.sh
```

# Using The WebApp
### Dashboard
The dashboard is where you will find all the important information about the server.
# Using The Server
### Connecting A New Device
New devices can be easily paired through the WebApp when the device is listed in the available connections.\
Another way to connect a device if an account has already been created and logged in, is to authenticate directly using the device.
### Authenticating With A Device
The pakcet of data sent will follow JSON syntax.
```json
{
  "type": "AUTHENTICATE",
  "username": "exampleUsername",
  "password": "examplePassword",
  "device": "exampleDeviceName",
  "devicetype": "both"
}
```
# Extensions
### Installing An Extension
### Extension Functions











