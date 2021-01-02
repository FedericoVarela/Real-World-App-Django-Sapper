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
            <button class="danger" on:click={deleteComment}>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-trash"
                    viewBox="0 0 16 16">
                    <path
                        d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
                    <path
                        fill-rule="evenodd"
                        d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
                </svg>
                DELETE</button>
        {/if}
        <button on:click={() => (reply === null ? (reply = '') : {})}>
            REPLY
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-reply"
                viewBox="0 0 16 16">
                <path
                    d="M9.502 5.013a.144.144 0 0 0-.202.134V6.3a.5.5 0 0 1-.5.5c-.667 0-2.013.005-3.3.822-.984.624-1.99 1.76-2.595 3.876C3.925 10.515 5.09 9.982 6.11 9.7a8.741 8.741 0 0 1 1.921-.306 7.403 7.403 0 0 1 .798.008h.013l.005.001h.001L8.8 9.9l.05-.498a.5.5 0 0 1 .45.498v1.153c0 .108.11.176.202.134l3.984-2.933a.494.494 0 0 1 .042-.028.147.147 0 0 0 0-.252.494.494 0 0 1-.042-.028L9.502 5.013zM8.3 10.386a7.745 7.745 0 0 0-1.923.277c-1.326.368-2.896 1.201-3.94 3.08a.5.5 0 0 1-.933-.305c.464-3.71 1.886-5.662 3.46-6.66 1.245-.79 2.527-.942 3.336-.971v-.66a1.144 1.144 0 0 1 1.767-.96l3.994 2.94a1.147 1.147 0 0 1 0 1.946l-3.994 2.94a1.144 1.144 0 0 1-1.767-.96v-.667z" />
            </svg>
        </button>
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
