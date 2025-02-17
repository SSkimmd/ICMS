export async function POST(event) {
    const data = await event.request.json();

    const request = await fetch("http://0.0.0.0:8081/extension", {
        signal: AbortSignal.timeout(3000),
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'debug'
        },
        body: JSON.stringify({
            "type": data['type'],
            "module": data['module']
        })
    });

    const response = await request.json();
    
    const newResponse = new Response();
    newResponse.json = response;
    return newResponse;
}