import { redirect } from '@sveltejs/kit'

export const handle = async({ event, resolve }) => {
    const requestedPath = event.url.pathname;
    const authorization = event.cookies.get('Authorization');

    if(!authorization && requestedPath == "/api/login") {
        return await resolve(event);
    }

    if(!authorization && requestedPath != "/login") {
        return new Response('Unauthorized', {
            status: 401,            
        })
    } else if(authorization && requestedPath == "/login") {
        throw redirect(302, '/dashboard');
    }

    return await resolve(event);
}