import { json } from '@sveltejs/kit'
import { GetURL } from '../../../lib/server/urls.server.js';

export async function GET(event) {
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const url = await GetURL();
    const response = await fetch(url + "devices", {
        method: 'GET',
        headers: {
            'Authorization': token
        }
    });

    const jsonResponse = await response.json();
    return json(jsonResponse);
}

export async function POST(event) {
    const data = await event.request.json();
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const url = await GetURL();
    const response = await fetch(url + "devices/add", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: JSON.stringify({
            "connection_name": data["connection_name"],
            "device_name": data["device_name"],
            "device_type": data["device_type"]
        })
    });

    const jsonResponse = await response.json();

    const requestResult = {
        "status": response.status,
        "response": jsonResponse
    };

    return json(requestResult);
}