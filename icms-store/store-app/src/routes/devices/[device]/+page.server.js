import { redirect } from '@sveltejs/kit';

export const load = async ({ params, fetch }) => {
    const device_name = params["device"];
    const response = await fetch("/api/store/devices");
    const data = response.json;
    const device = data[device_name]

    if(device == undefined) {
        throw redirect(301, "/devices");
    }

    return { ...device, 'device_name': device_name }
}

export const actions = {
    download: async({ request, fetch }) => {
        const data = await request.formData();
        const device = await data.get('device');
        const response = await fetch("/api/store/devices/download", {
            method: "POST",
            body: JSON.stringify({
                'device': device
            })
        })

        return response;
    }
}