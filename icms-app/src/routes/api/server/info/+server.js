export async function GET(event) {
    const auth = event.cookies.get("Authorization");
    const token = auth.split(" ")[1];

    const response = await fetch("http://0.0.0.0:8081/server/info", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        }
    });

    const jsonResponse = await response.json();
    const res = new Response();
    res.json = jsonResponse;

    return res;
}
