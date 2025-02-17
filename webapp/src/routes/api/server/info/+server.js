export async function GET(event) {
    const response = await fetch("http://0.0.0.0:8081/server/info", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'debug'
        }
    });

    const jsonResponse = await response.json();
    const res = new Response();
    res.json = jsonResponse;

    return res;
}
