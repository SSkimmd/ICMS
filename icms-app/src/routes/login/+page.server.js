import { redirect } from '@sveltejs/kit';

export const actions = {
    login: async({ request, cookies, fetch }) => {
        const data = await request.formData();
        const username = data.get('username');
        const password = data.get('password');

        const response = await fetch("/api/login", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "username": username,
                "password": password
            })
        }); 

        if(response.ok) {
            const token = await response.json();

            cookies.set('Authorization', `Bearer ${token['token']}`, {
                httpOnly: true,
                path: '/',
                secure: false,
                sameSite: 'strict',
                maxAge: 60 * 60 * 24 // 1 day
            });

            throw redirect(302, '/dashboard');
        }
        

        return;
    }
}