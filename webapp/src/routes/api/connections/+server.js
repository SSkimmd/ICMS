import { json } from '@sveltejs/kit'

export async function GET(event) {
    const response = await fetch("http://0.0.0.0:8081/connections", {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            'Authorization': 'debug'
        }
    });
    const jsonResponse = await response.json();
    return json(jsonResponse);
}