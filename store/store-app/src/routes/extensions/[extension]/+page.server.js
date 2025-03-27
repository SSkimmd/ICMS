import { redirect } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const extension_name = params["extension"];
    const response = await fetch("/api/store/extensions");
    const data = response.json;
    const extension = data[extension_name]

    if(extension == undefined) {
        throw redirect(301, "/extensions");
    }

    return { ...extension, 'extension_name': extension_name }
}

export const actions = {
}