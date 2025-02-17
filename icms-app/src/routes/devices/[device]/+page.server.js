export const load = async ({ params }) => {
    try {
        var server_info_response = await fetch("/api/server/info");
        const server_info = { ...server_info_response.json }

        if(!server_info["server_running"]) { return { "server_down": true } }

        let device_name = params["device"];
        device_name = device_name.replace("%20", " ");

        var response = await fetch("/api/devices", {
            signal: AbortSignal.timeout(3000),
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        return { ...data[device_name] }
    } catch { 
        return {}
    }
}


//                    <input placeholder="Enter String..." class="text-xl h-8 w-48 bg-inherit"/>