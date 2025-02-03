export const load = async () => {

    try {
        var response = await fetch("http://0.0.0.0:8081/server-info", {
            signal: AbortSignal.timeout(3000),
            method: 'GET'
        });

        const server_info = await response.json();
        if(!server_info["server_running"]) { return { "server_down": true } }

        var device_response = await fetch("http://0.0.0.0:8081/devices", {
            signal: AbortSignal.timeout(3000),
            method: 'GET',
            headers: {
                "Content-Type": "application/json"
            }
        });

        const devices = await device_response.json();
        
        var connection_response = await fetch("http://0.0.0.0:8081/connections", {
            signal: AbortSignal.timeout(3000),
            method: 'GET',
            headers: {
                "Content-Type": "application/json"
            }
        });

        const connections = await connection_response.json();

        return { "devices": devices, "connections": connections }
    } catch {
        return { "server_down": true }
    }
}