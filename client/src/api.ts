import axios from "axios";
import type { Response, Token, Paginated } from "./types"
import { match } from "./utils"

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
            result: res.data,
        }
    } catch (error) {
        return {
            result: new Error(error.request.response)
        }
    }
}

export async function get<T>(path: string, headers = {}): Response<T> {
    /* 
    Makes a call to the backend passing this.fetch as a callback
    @return: An object with the data and if the result is ok or an error
    */
    try {
        const res = await axios.get(apiRoot(path), {
            headers
        })

        return {
            result: res.data
        }
    } catch (err) {
        return {
            result: err
        }
    }
}

export async function paginated_get<T>(path: string, headers = {}, page?: number): Response<Paginated<T>> {
    /* Utility to encapsulate data from paginated endpoints */
    const queryParameters = page ? "&page=" + page : ""

    try {
        const res = await axios.get(apiRoot(path) + queryParameters, {
            headers
        })
        return {
            result: res.data
        }
    } catch (err) {
        return {
            result: err
        }
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
        try {
            const res = await axios.patch(apiRoot(path), body, {
                headers: this.getAuthHeader()
            })
            return { result: res.data }
        } catch (error) {
            return { result: error }
        }
    }

    async delete_(path) {
        try {
            const res = await axios.delete(apiRoot(path), {
                headers: this.getAuthHeader()
            })
            return res.data
        } catch (error) {
            return error
        }
    }

    async paginated_get(path: string, page?: number) {
        if (page) {
            return paginated_get(path, this.getAuthHeader(), page)
        } else {
            return paginated_get(path, this.getAuthHeader())
        }

    }

    static async login(username, password): Response<User> {
        const res = await post<Token>("jwt/create", {
            username,
            password,
        });

        return {
            result: match(
                res,
                (tk: Token) => new User(tk, username),
                (err: Error) => err
            )
        }
    }

    getAuthHeader() {
        return { "Authorization": `Bearer ${this.access_token}` }
    }
}