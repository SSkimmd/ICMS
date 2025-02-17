import { json } from '@sveltejs/kit'

export async function POST(event) {
    const data = await event.request.json();

    const jsonData = JSON.stringify({
        "device": data["device"],
        "function": data["function"],
        "arguments": data["arguments"]
    })

    const response = await fetch("http://0.0.0.0:8081/device", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'debug'
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