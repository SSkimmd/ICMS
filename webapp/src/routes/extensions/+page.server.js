export const load = async () => {
    try {
        var response = await fetch("http://0.0.0.0:8081/server-info", {
            signal: AbortSignal.timeout(3000),
            method: 'GET'
        });

        const server_info = await response.json();
        if(!server_info["server_running"]) { return; }


        var response = await fetch("http://0.0.0.0:8080/", {
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
        return { ...data }
    } catch { 
        return {}
    }
}