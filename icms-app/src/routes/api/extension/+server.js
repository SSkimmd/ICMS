import { GetURL } from '../../../lib/server/urls.server.js'

export async function POST(event) {
    const data = await event.request.json();
    
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const url = await GetURL();
    const request = await fetch(url + "extension", {
        signal: AbortSignal.timeout(3000),
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: JSON.stringify({
            "type": data['type'],
            "module": data['module']
        })
    });

    const response = await request.json();
    
    const newResponse = new Response();
    newResponse.json = response;
    return newResponse;
}