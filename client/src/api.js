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
    /* 
    Makes a call to the backend passing this.fetch as a callback
    @return: An object with the data and if the result is ok or an error
    */
    try {
        const res = await fn(apiRoot(path), {
            headers
        })
        const data = await res.json()
        return {data, ok: res.ok}
    } catch (error) {
        throw new Error(error)
    }
}

export class User {
    constructor(token) {
        this.refresh_token = token.refresh
        this.access_token = token.access
    }

    async post(path, body) {
        return post(path, body, this.getAuthHeader())
    }

    static async login(username, password) {
        const res = await post("jwt/create", {
            username,
            password,
        });
        const user = new User(res)
        return user
         
    }

    async refreshToken() {
        const res = await post("jwt/refresh", {"refresh": this.refresh_token})
        this.access_token = res.refresh
    }

    getAuthHeader() {
        return {"Authorization": `Bearer ${this.access_token}`}
    }

}