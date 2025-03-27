import { GetURL } from '../../../lib/server/urls.server.js'

export async function POST(event) {
    try {
        const url = await GetURL();
        const data = await event.request.json();
        const response = await fetch(url + "login", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": data["username"],
                "password": data["password"]
            })
        });

        const token = await response.json();
        return new Response(JSON.stringify(token));
    } catch {
        const res = new Response();
        res.status = 500;
        return res;
    }
}
