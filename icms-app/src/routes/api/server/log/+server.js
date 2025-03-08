import { error, json, text } from '@sveltejs/kit'

export async function POST(event) {
    const data = await event.request.json();
    
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    try {
        const response = await fetch("http://0.0.0.0:8081/server/log", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({
                "lines": data['lines']
            })
        });

        const textResponse = await response.text();
        return new Response(textResponse);
    } catch {
        return new Response('Server Is Offline');
    }
}