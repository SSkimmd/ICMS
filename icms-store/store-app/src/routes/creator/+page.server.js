import { redirect, error } from '@sveltejs/kit'


export const load = async ({ fetch }) => {
}

export const actions = {
    upload: async({ request, cookies, fetch }) => {
        const data = await request.formData();
        const file = await data.get('fileInput');
        const name = await data.get('name');
        const type = await data.get('type');

        const types = ["extension", "device"]
        if(!types.includes(type)) {
            return;
        }

        if(name.includes(' ')) {
            return;
        }

        if(!name.length > 0) {
            return;
        }

        const form = new FormData();
        form.append('file', file);
        form.append('name', name)
        form.append('type', type)

        const response = await fetch('/api/store/upload/' + name, {
            method: "POST",
            body: form
        })

        console.log(response.status);
    }
}