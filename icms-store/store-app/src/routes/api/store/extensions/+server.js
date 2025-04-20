import { json } from '@sveltejs/kit'
import { SERVER_URL } from '$env/static/private'

export async function GET(event) {
    //const auth = event.cookies.get("Authorization");
    //const token = auth.split(" ")[1];

    const response = await fetch(SERVER_URL + "extensions", {
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