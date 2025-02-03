import { json } from '@sveltejs/kit'

export async function GET(event) {
    const data = await event.request.json();

    const response = await fetch("http://0.0.0.0:8081/devices", {
        method: 'GET'
    });

    const jsonResponse = await response.json();
    return json(jsonResponse);
}

export async function POST(event) {
    const data = await event.request.json();

    const response = await fetch("http://0.0.0.0:8081/devices/add", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
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