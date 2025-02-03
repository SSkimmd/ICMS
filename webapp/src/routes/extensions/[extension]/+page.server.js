export const load = async ({ params }) => {
    try {
        var response = await fetch("http://0.0.0.0:8081/server-info", {
            signal: AbortSignal.timeout(3000),
            method: 'GET'
        });

        const server_info = await response.json();
        if(!server_info["server_running"]) { return; }

        let extension_name = params["extension"];

        var response = await fetch("http://0.0.0.0:8081/extension", {
            signal: AbortSignal.timeout(3000),
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "type": "GET",
                "module": "all"
            })
        });
        const data = await response.json();
        data[extension_name]["extension"] = extension_name;
        return { ...data[extension_name] }
    } catch { 
        return {}
    }
}