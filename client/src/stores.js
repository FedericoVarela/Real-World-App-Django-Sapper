import { writable } from "svelte/store"

export const profileStore = writable({
    username: null,
    email: null,
    id: null,
}) 