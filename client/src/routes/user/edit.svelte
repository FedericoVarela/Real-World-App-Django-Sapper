<script context="module" lang="ts">
    // import { preload } from "./profile.svelte"
    //TODO: Figure out how to avoid naming collision
    import type { Profile } from "../../types";
    import { get } from "../../api";
    import { match } from "../../utils";

    export async function preload(page, session) {
        if (session.user === undefined) {
            return this.redirect(302, "user/login");
        } else {
            const res = await get<Profile>(`profile/${session.user.username}`, {
                Authorization: `Bearer ${session.user.access_token}`,
            });

            return match(
                res,
                (data: Profile) => {
                    return { data };
                },
                (err) => {
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
        const res = $session.user.patch("settings", {
            username,
            description,
            picture,
        });
        match(
            res,
            (_) => goto("user/profile"),
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
