import { redirect } from '@sveltejs/kit'

export const handle = async({ event, resolve }) => {
    const requestedPath = event.url.pathname;
    const authorization = event.cookies.get('Authorization');

    if(!authorization) {
        if(requestedPath != "/api/login" && requestedPath != "/login") {
            throw redirect(302, '/login');
        }
    } else {
        const token = authorization.split(' ')[1];

        if(token == 'undefined' && requestedPath != '/login') {
            throw redirect(302, '/login');
        }
        if(token != 'undefined' && requestedPath == '/login') {
            throw redirect(302, '/dashboard');
        }
    }


    return await resolve(event);
}