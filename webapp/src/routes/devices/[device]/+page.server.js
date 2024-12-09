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

        var response = await fetch("http://0.0.0.0:8080/", {
            signal: AbortSignal.timeout(3000),
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "type": "GET",
                "device": "all"
            })
        });
        const data = await response.json();
        data["devices"][device_name]["device"] = device_name;
        return { ...data["devices"][device_name] }
    } catch { 
        return {}
    }
}


//                    <input placeholder="Enter String..." class="text-xl h-8 w-48 bg-inherit"/>