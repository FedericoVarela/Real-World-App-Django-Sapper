import axios from "axios";

export const apiRoot = (path) => `http://localhost:8000/api/v0/${path}/?format=json`


export async function post(path, body, headers = {}) {
    try {
        const res = await axios({
            method: "POST",
            url: apiRoot(path),
            data: body,
            headers,
        })
        const { data } = res
        return data
    } catch (error) {
        throw new Error(error.response.status)
    }
}

export async function get(fn, path, headers={}) {
    try {
        const res = await fn(apiRoot(path), {
            headers
        })
        const data = await res.json()
        return data
    } catch (error) {
        throw new Error(error)
    }
}

export class User {
    constructor(token) {
        this.refresh_token = token.refresh
        this.access_token = token.access
    }

    async refreshToken() {
        console.log("Refresh")
        console.log(this.refresh_token)
        const res = await post("jwt/refresh", {"refresh": this.refresh_token})
        console.log("El token es" + res)
    }

}