export const load = async ({ fetch }) => {
    const response = await fetch("/api/store/extensions");
    const data = response.json;
    return { ...data }
}

export const actions = {
}