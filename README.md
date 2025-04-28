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
### Manually
Installation on a windows system will by default require the usage of WSL.\


# Usage
When starting the application using Docker a link to the webapp will be displayed along with the port being exposed.\

# Manually
When using the applications, both applications will need to be started manually.
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













