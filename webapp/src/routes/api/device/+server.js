import { json } from '@sveltejs/kit'

export async function POST(event) {
    const data = await event.request.json();

    const response = await fetch("http://0.0.0.0:8081/device", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "device": data["device"],
            "message": data["message"]
        })
    });

    const jsonResponse = await response.json();

    const requestResult = {
        "status": response.status,
        "response": jsonResponse
    };
    return json(requestResult);
}