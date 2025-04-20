export const load = async ({ params, fetch }) => {
    try {
        var server_info_response = await fetch("/api/server/info");
        const server_info = { ...server_info_response.json }

        if(!server_info["server_running"]) { return { "server_down": true } }

        const extension_name = params["extension"];
        const extension_request = await fetch("/api/extension", { 
            method: 'POST',
            body: JSON.stringify({
                "type": "GET",
                "module": "all"
            })
        })

        const data = { ...extension_request.json };
        return { ...data[extension_name], "name": extension_name }
    } catch { 
        return {}
    }
}