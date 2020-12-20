<script lang="ts">
    import { stores } from "@sapper/app";
    import { createEventDispatcher } from "svelte";
    import type { Comment, Option } from "../types";
    import { match } from "../utils";
    import type { Node } from "../comments";

    export let data: Comment;
    export let post_id: number;
    export let children: Node[] = [];

    const dispatch = createEventDispatcher();
    const { session } = stores();
    const { content, author, id, created_at } = data;
    let reply: Option<string> = null;

    async function deleteComment() {
        dispatch("delete", {
            id,
        });
    }

    async function postReply() {
        const res = await $session.user.post("posts/" + post_id + "/comments", {
            content: reply,
            reply_to: id,
        });
        match(
            res,
            (comment: Comment) => {
                dispatch("reply", { id, comment });
                reply = null;
            },
            (error: Error) => dispatch("error", { error })
        );
    }

    function forwardEvent(event) {    
        dispatch(event.type, event.detail)
    }
</script>

<style>
    img {
        width: 70px;
        height: auto;
    }
</style>

{content}
<em>By {author.username}</em>
<img src={author.picture} alt={author.username + "'s profile picture"} />
{created_at}
<!-- Controls -->
{#if $session.user}
    {#if author.username == $session.user.username}
        <button on:click={deleteComment}>DELETE</button>
    {/if}
    <button on:click={() => (reply === null ? (reply = '') : {})}>REPLY</button>
    {#if reply !== null}
        <button on:click={() => (reply = null)}>CANCEL</button>
        <input type="text" bind:value={reply} />
        <button on:click={postReply}>SUBMIT</button>
    {/if}
{/if}

{#each children as { data, children }}
    <svelte:self
        {data}
        {post_id}
        {children}
        on:delete={forwardEvent}
        on:reply={forwardEvent}
        on:error={forwardEvent} />
{/each}

<hr />
