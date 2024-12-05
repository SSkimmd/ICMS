export const load = async () => {
    try {
        const response = await fetch("http://0.0.0.0:8081/server-info", {
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
        await fetch("http://0.0.0.0:8081/start", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });      
    },
    stop: async(event) => {
        await fetch("http://0.0.0.0:8081/stop", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }); 
    },
    restart: async(event) => {
        await fetch("http://0.0.0.0:8081/restart", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }); 
    }
}