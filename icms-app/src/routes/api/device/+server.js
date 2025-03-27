import { json } from '@sveltejs/kit'
import { GetURL } from '../../../lib/server/urls.server.js';

export async function POST(event) {
    const data = await event.request.json();
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const jsonData = JSON.stringify({
        "device": data["device"],
        "function": data["function"],
        "arguments": data["arguments"]
    })

    const url = await GetURL();
    const response = await fetch(url + "device", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: jsonData
    });

    const jsonResponse = await response.json();

    const requestResult = {
        "status": response.status,
        "response": jsonResponse
    };

    return json(requestResult);
}