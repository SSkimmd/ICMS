export const load = async () => {
    try {
        const response = await fetch("http://0.0.0.0:8081/serverInfo", {
            signal: AbortSignal.timeout(3000),
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        return { ...data }
    } catch {
        return { }
    }
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