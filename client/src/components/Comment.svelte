<script lang="ts">
    import { stores } from "@sapper/app";
    import { createEventDispatcher } from "svelte";

    import type { Comment } from "../types";

    export let data: Comment;

    const dispatch = createEventDispatcher();
    const { session } = stores();

    async function deleteComment() {
        dispatch("delete", {
            id: data.id,
        });
    }
</script>

{data.content}
<em>By {data.author.username}</em>
<img
    src={data.author.picture}
    alt={data.author.username + "'s profile picture"} />
{data.created_at}
{#if $session.user && data.author.username == $session.user.username}
    <button on:click={deleteComment}>DELETE</button>
{/if}
