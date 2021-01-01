<script lang="ts">
    import { stores } from "@sapper/app";
    import { createEventDispatcher } from "svelte";
    import type { Comment, Option } from "../types";
    import { match } from "../utils";
    import type { Node } from "../comments";

    export let data: Comment;
    export let post_id: number;
    export let children: Node[] = [];
    export let level = 0;

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
        dispatch(event.type, event.detail);
    }
</script>

<style>
    img {
        width: 45px;
        height: auto;
        border-radius: 100%;
    }

    header > em {
        position: absolute;
        margin-left: 20px;
    }

    div {
        box-shadow: 0 2px 9px 0 rgba(0, 0, 0, 0.25);
        border-radius: 15px;
        padding: 12px 20px;
        margin-top: 12px;
    }

    section {
        margin-top: 5px;
    }
    button {
        margin-right: 10px;
    }
</style>

<div style={'margin-left: ' + 25 * level + 'px;'}>
    <header>
        <img
            src={author.picture}
            alt={author.username + "'s profile picture"} />
        <em>By {author.username} at {new Date(created_at).toUTCString()}</em>
    </header>
    <p>{content}</p>
    <!-- Controls -->
    {#if $session.user}
        {#if author.username == $session.user.username}
            <button class="danger" on:click={deleteComment}>DELETE</button>
        {/if}
        <button
            on:click={() => (reply === null ? (reply = '') : {})}>REPLY</button>
        {#if reply !== null}
            <section>
                <input type="text" bind:value={reply} />
                <button
                    class="danger"
                    on:click={() => (reply = null)}>CANCEL</button>
                <button on:click={postReply}>SUBMIT</button>
            </section>
        {/if}
    {/if}
</div>

{#each children as { data, children }}
    <svelte:self
        level={level + 1}
        {data}
        {post_id}
        {children}
        on:delete={forwardEvent}
        on:reply={forwardEvent}
        on:error={forwardEvent} />
{/each}
