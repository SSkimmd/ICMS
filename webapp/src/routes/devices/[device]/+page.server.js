export const load = async ({ params }) => {
    try {
        var response = await fetch("http://0.0.0.0:8081/server-info", {
            signal: AbortSignal.timeout(3000),
            method: 'GET'
        });

        const server_info = await response.json();
        if(!server_info["server_running"]) { return; }

        let device_name = params["device"];
        device_name = device_name.replace("%20", " ");

        var response = await fetch("http://0.0.0.0:8081/devices", {
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