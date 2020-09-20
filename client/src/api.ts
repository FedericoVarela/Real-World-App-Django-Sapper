import axios from "axios";

interface Response {
    data: string,
    ok: boolean
}

type Result = Response | Error

export function isOK(item: Result) : boolean {
    return !(item instanceof Error)
}

export const apiRoot : (string) => string = (path) => `http://localhost:8000/api/v0/${path}/?format=json`

export async function post(path, body, headers = {}): Promise<Result> {
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
        let response = JSON.parse(error.request.response)        
        if ("username" in response) {
            return new Error("A user with that username already exists.")
        }        
        return error
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

export async function patch(path, body, headers={}) : Promise<Result> {
    try {
        const res = await axios.patch(apiRoot(path), body, {
            headers
        })
        return res.data
    } catch (error) {
        return error
    }
}

export class User {

    refresh_token: string
    access_token: string
    username: string

    constructor(token, username: string) {
        this.refresh_token = token.refresh
        this.access_token = token.access
        this.username = username
    }

    async post(path, body) : Promise<Result> {
        return post(path, body, this.getAuthHeader())
    }

    async patch(path, body) : Promise<Result> {
        return patch(path, body, this.getAuthHeader())
    }

    static async login(username, password) : Promise<User> {
        const res = await post("jwt/create", {
            username,
            password,
        });
        const user = new User(res, username)
        console.log(user);
        return user
         
    }

    getAuthHeader() {
        return {"Authorization": `Bearer ${this.access_token}`}
    }

    

}