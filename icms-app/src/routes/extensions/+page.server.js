export const load = async ({ fetch }) => {
    try {
        var server_info_response = await fetch("/api/server/info");
        const server_info = { ...server_info_response.json }

        if(!server_info["server_running"]) { return { "server_down": true } }

        var extension_response = await fetch("/api/extensions");
        const extensions = { ...extension_response.json }

        return { ...extensions["extensions"] }
    } catch {
        return { 'server_down': true };
    }
}