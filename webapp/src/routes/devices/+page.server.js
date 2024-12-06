export const load = async () => {
    try {
        const response = await fetch("http://0.0.0.0:8080/", {
            signal: AbortSignal.timeout(3000),
            method: 'POST',
            body: {
                "type": "GET",
                "devices": "all"
            },
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log(data);
        return { ...data }
    } catch {
        return { }
    }
}


export const actions = {
    GetDevices: async(event) => {
        await fetch("http://0.0.0.0:8081/start", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });      
    },
}