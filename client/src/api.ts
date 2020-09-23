import axios from "axios";
import type { Response, Token } from "./types"
import { unwrap } from "./utils"

export const apiRoot = (path: string) => `http://localhost:8000/api/v0/${path}/?format=json`

export async function post<T>(path: string, body: object, headers = {}): Response<T> {
    try {
        const res = await axios({
            method: "POST",
            url: apiRoot(path),
            data: body,
            headers,
        })
        return {
            result: res,
        }
    } catch (error) {
        let response = JSON.parse(error.request.response)
        if ("username" in response) {
            return {
                result: { data: new Error("A user with that username already exists.") }
            }
        }
        return {
            result: { data: new Error(error.request.response), }
        }
    }
}

export async function get<T>(path: string, headers = {}): Response<T> {
    /* 
    Makes a call to the backend passing this.fetch as a callback
    @return: An object with the data and if the result is ok or an error
    */
    // try {
    //     const res = await fn(apiRoot(path), {
    //         headers
    //     })
    //     const data = await res.json()
    //     return { data, ok: res.ok }
    // } catch (error) {
    //     throw new Error(error)
    // }
    try {
        const res = await axios.get(apiRoot(path), {
            headers
        })
        return {
            result: res
        }
    } catch (err) {
        return err
    }
}

async function patch<T>(path, body, headers = {}): Response<T> {
    try {
        const res = await axios.patch(apiRoot(path), body, {
            headers
        })
        return res.data
    } catch (error) {
        return error
    }
}

async function delete_<T>(path, headers = {}): Response<T> {
    try {
        const res = await axios.delete(apiRoot(path), {
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

    constructor(token: Token, username: string) {
        this.refresh_token = token.refresh
        this.access_token = token.access
        this.username = username
    }

    async post<T>(path: string, body): Response<T> {
        return post(path, body, this.getAuthHeader())
    }

    async patch<T>(path, body): Response<T> {
        return patch(path, body, this.getAuthHeader())
    }

    async delete_(path) {
        return delete_(path, this.getAuthHeader())
    }

    static async login(username, password): Promise<User> {
        const res = await post<Token>("jwt/create", {
            username,
            password,
        });
        const data = unwrap(res).data
        const user = new User(data, username)
        return user
    }

    getAuthHeader() {
        return { "Authorization": `Bearer ${this.access_token}` }
    }
}