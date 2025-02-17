import { json } from '@sveltejs/kit'

export async function POST(event) {
    const data = await event.request.json();

    const request = await fetch("http://0.0.0.0:8081/extensions", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'debug'
        },
        body: JSON.stringify({
            "type": data["type"],
            "module": data["module"],
            "function": data["function"],
            "arguments": data["arguments"]
        })
    });

    const jsonResponse = await request.json();

    return json(JSON.stringify({
        "status": request.status,
        "message": jsonResponse
    })); 
}

export async function GET(event) {
    const request = await fetch("http://0.0.0.0:8081/extensions", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'debug'
        }
    });

    const jsonResponse = await request.json();
    const res = new Response();
    res.json = jsonResponse;

    return res; 
}

