import { redirect } from '@sveltejs/kit'


export const load = async ({ fetch }) => {
}

export const actions = {
    upload: async({ request, cookies }) => {
        const data = await request.formData();
        const file = await data.get('fileInput');

        const form = new FormData();
        form.append('file', file);

        const response = await fetch('http://0.0.0.0:8082/extensions/upload', {
            method: "POST",
            body: form
        })

        console.log(response.status);
    }
}