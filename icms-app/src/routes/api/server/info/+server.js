import { GetURL } from '../../../../lib/server/urls.server.js';

export async function GET(event) {
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const url = await GetURL();
    const response = await fetch(url + "server/info", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        }
    });

    const jsonResponse = await response.json();
    const res = new Response();
    res.json = jsonResponse;

    return res;
}
