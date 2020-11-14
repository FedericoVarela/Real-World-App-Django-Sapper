<script lang="ts">
    import { stores } from "@sapper/app";
    import { createEventDispatcher } from "svelte";

    import type { Comment } from "../types";
    import { match } from "../utils";

    export let data: Comment;

    const dispatch = createEventDispatcher();
    const { session } = stores();

    async function deleteComment() {
        const res = $session.user.delete_(`comment/delete/${data.id}`);
        match(
            res,
            (_) => {
                dispatch("delete", {
                    id: data.id,
                });
            },
            (err: Error) => {
                throw err;
            }
        );
    }
</script>



{data.content}
<em>By {data.author.username}</em>
{data.created_at}
{#if $session.user && data.author.username == $session.user.username}
    <button on:click={deleteComment}>DELETE</button>
{/if}
