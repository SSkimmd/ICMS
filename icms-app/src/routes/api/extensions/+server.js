import { json } from '@sveltejs/kit'

export async function POST(event) {
    const data = await event.request.json();
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const request = await fetch("http://0.0.0.0:8081/extensions", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
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
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const request = await fetch("http://0.0.0.0:8081/extensions", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        }
    });

    const jsonResponse = await request.json();
    const res = new Response();
    res.json = jsonResponse;

    return res; 
}

