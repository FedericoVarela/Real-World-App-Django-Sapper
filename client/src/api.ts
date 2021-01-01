import axios from "axios";
import type { Response, Token, Paginated, Session } from "./types"
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
        const code = error.response.data.code
        return {
            result: new Error(code === "token_not_valid" ? "token_not_valid" : error.request.response)
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
    } catch (error) {
        const code = error.response.data.code
        return {
            result: new Error(code === "token_not_valid" ? "token_not_valid" : error.request.response)
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
    } catch (error) {
        const code = error.response.data.code
        return {
            result: new Error(code === "token_not_valid" ? "token_not_valid" : error.request.response)
        }
    }
}


export async function maybe_authorized_get<T>(path: string, user: Session): Response<T> {
    if (!user) {
        return get<T>(path, {})
    } else {
        return user.get<T>(path)
    }
}


export async function maybe_authorized_paginated_get<T>(path: string, user: Session, page?: number): Response<Paginated<T>> {
    if (!user) {
        return paginated_get<T>(path, {}, page)
    } else {
        return user.paginated_get<T>(path, page)
    }
}


export class User {

    refreshToken: string
    accessToken: string
    username: string

    constructor(token: Token, username: string) {
        this.refreshToken = token.refresh
        this.accessToken = token.access
        this.username = username
    }


    static async refresh(refresh: string): Response<Token> {
        try {
            const res = await axios({
                method: "POST",
                url: apiRoot("jwt/refresh"),
                data: { refresh },
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


    static async fromSession(): Promise<Session> {
        const username = localStorage.getItem("username")
        const refresh = localStorage.getItem("refresh")
        if (username !== null) {
            const token = match(
                await User.refresh(refresh),
                (tk: Token) => tk,
                (_: Error) => {
                    return null
                }
            )
            return (token === null ? undefined : new User(token, username))
        } else {
            //? Although null makes more sense, the application identifies undefined as the anonymus user
            return undefined
        }
    }


    async tryRefresh<T>(callback: () => Response<T>): Response<T> {

        return match(
            await callback(),
            (ok: T) => {
                return { result: ok }
            },
            async (err: Error) => {
                if (err.message === "token_not_valid") {
                    return match(
                        await User.refresh(this.refreshToken),
                        ({ access, refresh }) => {
                            this.refreshToken = refresh
                            localStorage.setItem("refresh", refresh)
                            this.accessToken = access
                            return callback()
                        },
                        (err: Error) => {
                            return { result: err }
                        }

                    )
                } else {
                    return { result: err }
                }
            }
        )
    }

    async get<T>(path: string): Response<T> {
        return this.tryRefresh(() => get<T>(path, this.getAuthHeader()))
    }

    async post<T>(path: string, body): Response<T> {
        return this.tryRefresh(() => post(path, body, this.getAuthHeader()))
    }

    async patch<T>(path, body): Response<T> {
        const patchFn = async () => {
            try {
                const res = await axios.patch(apiRoot(path), body, {
                    headers: this.getAuthHeader()
                })
                return { result: res.data }
            } catch (error) {
                const code = error.response.data.code
                return {
                    result: new Error(code === "token_not_valid" ? "token_not_valid" : error.request.response)
                }
            }
        }

        return this.tryRefresh(patchFn)
    }

    async delete_<T>(path): Response<T> {
        const deleteFn = async () => {
            try {
                const res = await axios.delete(apiRoot(path), {
                    headers: this.getAuthHeader()
                })
                return res.data
            } catch (error) {
                const code = error.response.data.code
                return {
                    result: new Error(code === "token_not_valid" ? "token_not_valid" : error.request.response)
                }
            }
        }
        return this.tryRefresh(deleteFn)
    }

    async paginated_get<T>(path: string, page?: number): Response<Paginated<T>> {
        return this.tryRefresh(() => (page ? paginated_get(path, this.getAuthHeader(), page) : paginated_get(path, this.getAuthHeader())))
    }

    static async login(username, password): Response<User> {
        const res = await post<Token>("jwt/create", {
            username,
            password,
        });

        return {
            result: match(
                res,
                (tk: Token) => {
                    localStorage.setItem("username", username)
                    localStorage.setItem("refresh", tk.refresh)
                    return new User(tk, username)
                },
                (err: Error) => err
            )
        }
    }



    getAuthHeader() {
        return { "Authorization": `Bearer ${this.accessToken}` }
    }
}