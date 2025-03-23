import { redirect } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const device_name = params["device"];
    const response = await fetch("/api/store/devices");
    const data = response.json;
    const device = data[device_name]

    if(device == undefined) {
        throw redirect(301, "/devices");
    }

    return { ...device }
}

export const actions = {
    
}