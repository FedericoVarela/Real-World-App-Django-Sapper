<script lang="ts">
    import { stores, goto } from "@sapper/app";
    import { match } from "../utils";

    const { session } = stores();
    export let is_favorite: boolean;
    export let id;
    
    async function toggleFavorite() {
        if (!$session.user) {
            await goto("user/login");
        }

        if (!is_favorite) {
            const res = $session.user.post("favorites", { id });
            match(
                res,
                (_) => (is_favorite = true),
                (err: Error) => {
                    throw err;
                }
            );
        } else {
            const res = $session.user.delete_("favorites/" + id)
            match(
                res,
                (_) => (is_favorite = false),
                (err: Error) => {
                    throw err;
                }
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

<button on:click={toggleFavorite} class:active={is_favorite}> ♥ </button>
