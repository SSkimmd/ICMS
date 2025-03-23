import { json } from '@sveltejs/kit'

export async function GET(event) {
    //const auth = event.cookies.get("Authorization");
    //const token = auth.split(" ")[1];

    const response = await fetch("http://0.0.0.0:8082/devices", {
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        }
    });
    const jsonResponse = await response.json();
    const serverResponse = new Response();
    serverResponse.json = jsonResponse;
    return serverResponse;
}