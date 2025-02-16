export const load = async () => {
    try {
        var response = await fetch("http://0.0.0.0:8081/server/info", {
            signal: AbortSignal.timeout(3000),
            method: 'GET'
        });

        const server_info = await response.json();
        if(!server_info["server_running"]) { return { "server_down": true } }

        var response = await fetch("http://0.0.0.0:8081/extensions", {
            signal: AbortSignal.timeout(3000),
            method: 'GET'
        });
        
        const data = await response.json();
        return { ...data["extensions"] }
    } catch {
        return { 'server_down': true };
    }
}