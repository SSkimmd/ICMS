import { json } from '@sveltejs/kit'
import { SERVER_URL } from '$env/static/private'

export async function POST({ request }) {
    //const auth = event.cookies.get("Authorization");
    //const token = auth.split(" ")[1];
    //const requestJson = await request.json();
    let requestJson = await request.json();
    let deviceName = requestJson['device'];

    const response = await fetch(SERVER_URL + "devices/" + deviceName, {
        method: 'GET'
    });

    const files = await response.blob();

    return new Response(files, { status: 200, headers: {
        "Content-Type": 'application/octet-stream',
        "Content-Disposition": "attachment; filename=" + deviceName + ".zip"
    }});
}