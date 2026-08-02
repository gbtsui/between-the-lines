import {env} from "$env/dynamic/private";
import {SILLYMAXXED_INTERNAL_SERVER_SECRET} from "$env/static/private";

export const POST = async ({request, params}) => {
    const apiUrl = env.FLASK_API_URL || "http://localhost:6767"
    const path = params.path;

    console.log(`POST request called Svelte-side. API url ${apiUrl}, path ${path}`);

    const requestBody = await request.json()
    //console.log(`RequestBody: ${JSON.stringify(requestBody)}`)

    const response = await fetch(`${apiUrl}/${path}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Secret": SILLYMAXXED_INTERNAL_SERVER_SECRET
        },
        body: JSON.stringify(requestBody)
    })

    const data = await response.json()

    //console.log(`Response body: ${JSON.stringify(data)}`)

    return new Response(JSON.stringify(data), {
        headers: {"Content-Type": "application/json"}
    })
}

export const OPTIONS = () => {

    return new Response(null, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    });
}