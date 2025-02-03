import { json } from '@sveltejs/kit'

export async function GET(event) {
    console.log("the fuck??");
    const data = await event.request.json();

    const response = await fetch("http://0.0.0.0:8081/connections", {
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        }
    });
    const jsonResponse = await response.json();
    return json(jsonResponse);
}