import { DOCKER_SERVER_URL, LOCAL_SERVER_URL, URL_MODE } from '$env/static/private'

export async function GetURL() {
    if(URL_MODE == "local") {
        return LOCAL_SERVER_URL;
    } else if(URL_MODE == "docker") {
        return DOCKER_SERVER_URL;
    }
}