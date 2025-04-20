export const load = async ({ fetch }) => {
    const response = await fetch("/api/server/info");
    const data = response.json;
    return { ...data }
}

export const actions = {
    start: async(event) => {
        try {
            await fetch("http://0.0.0.0:8081/start", {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }); 
        } catch {

        }
    },
    stop: async(event) => {
        try {
            await fetch("http://0.0.0.0:8081/stop", {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        } catch {

        }
    },
    restart: async(event) => {
        try {
            await fetch("http://0.0.0.0:8081/restart", {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }); 
        } catch {

        }
    }
}