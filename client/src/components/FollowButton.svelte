<script lang="ts">
    import { stores, goto } from "@sapper/app";
    import type { Option } from "../types";
    import { match } from "../utils";
    import UIError from "./Error.svelte";

    export let username;
    export let is_following;

    const { session } = stores();

    let error: Option<Error> = null;

    async function toggleFollow() {
        if ($session.user.username === undefined) {
            await goto("user/login");
        }
        if (!is_following) {
            const res = $session.user.post("following", { username });
            match(
                res,
                () => {
                    is_following = true;
                    error = null;
                },
                (err: Error) => (error = err)
            );
        } else {
            const res = $session.user.delete_("following/" + username);
            match(
                res,
                () => {
                    is_following = false;
                    error = null;
                },
                (err: Error) => (error = err)
            );
        }
    }
</script>

<style>
    button {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>

{#if error}
    <UIError data={error} />
{/if}
<button on:click={toggleFollow} class:active={is_following}>
    +
    {is_following ? 'Unf' : 'F'}ollow
    {username}</button>
