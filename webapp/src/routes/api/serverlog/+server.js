import { error, json, text } from '@sveltejs/kit'

export async function POST(event) {
    const data = await event.request.json();

    try {
        const response = await fetch("http://0.0.0.0:8081/serverLog", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
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