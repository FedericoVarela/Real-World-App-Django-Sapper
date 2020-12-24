<script context="module" lang="ts">
    
    import type { Profile } from "../../types";
    import { match } from "../../utils";

    export async function preload(page, session) {
        if (session.user === undefined) {
            return this.redirect(302, "user/login");
        } else {
            const res = await session.user.get(`profile/${session.user.username}`)
            return match(
                res,
                (data: Profile) => {
                    return { data };
                },
                (err: Error) => {
                    throw err;
                }
            );
        }
    }
</script>

<script lang="ts">
    import { stores, goto } from "@sapper/app";
    import UIError from "../../components/Error.svelte";

    export let data: Profile;
    const { session } = stores();
    let { username, description, picture } = data;
    let error: Error;

    async function handleSubmit() {
        const res = await $session.user.patch("settings", {
            username,
            description,
            picture,
        });
        match(
            res,
            async (_) => {
                $session.user.username = username
                await goto("user/profile")
            },
            (err: Error) => (error = err)
        );
    }
</script>

{#if error}
    <UIError data={error} />
{/if}

<input type="text" bind:value={username} />
<input type="text" bind:value={description} />
<input type="url" bind:value={picture} />

<button on:click={handleSubmit}>SUBMIT</button>
