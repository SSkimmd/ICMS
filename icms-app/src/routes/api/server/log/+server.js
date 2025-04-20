import { error, json, text } from '@sveltejs/kit'
import { GetURL } from '../../../../lib/server/urls.server.js';

export async function POST(event) {
    const data = await event.request.json();
    
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    try {
        const url = await GetURL();
        const response = await fetch(url + "server/log", {
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