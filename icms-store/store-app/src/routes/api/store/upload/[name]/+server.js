import { redirect, error } from '@sveltejs/kit'
import { SERVER_URL } from '$env/static/private'

export async function POST({ request, params, url }) {
    try {
        const data = await request.formData();
        const type = await data.get('type') + "s";

        const response = await fetch(SERVER_URL + type + "/upload", {
            method: "POST",
            body: data
        });

        return response;
    } catch {
        throw error(400);
    }
}