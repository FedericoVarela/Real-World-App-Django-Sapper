<script lang="ts">
    import { stores } from "@sapper/app";
    import type { Option } from "../types";
    import { match } from "../utils";
    import UIError from "./Error.svelte";

    export let username;
    export let is_following;

    const { session } = stores();

    let error: Option<Error> = null;

    async function toggleFollow() {
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
    button.active {
        color: white;
        background-color: rgb(255, 62, 0);
    }
</style>

{#if error}
    <UIError data={error} />
{/if}
<button on:click={toggleFollow} class:active={is_following} >
    +
    {is_following ? 'Unf' : 'F'}ollow
    {username}</button>
