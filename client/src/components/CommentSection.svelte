<script lang="ts">
  import { stores } from "@sapper/app";

  import { match } from "../utils";
  import { paginated_get } from "../api";
  import type { Comment, Paginated, Result, Option } from "../types";
  import { CommentTree } from "../comments";

  import UIComment from "./Comment.svelte";
  import Modal from "./Modal.svelte";
  import UIError from "./Error.svelte";

  export let post_id: number;

  const { session } = stores();
  const endpoint = `posts/${post_id}/comments`;
  let comment;
  let comment_list: Comment[] = [];
  let next: Option<string>;
  let error: Error;
  // Comment whose deletion is being confirmed, if any
  let deleteTarget: Option<number> = null;

  $: comment_tree = new CommentTree(comment_list);

  const comment_promise = paginated_get<Comment>(endpoint).then((data) => {
    match(
      data,
      (comments: Paginated<Comment>) => {
        comment_list = [...comment_list, ...comments.results];
        next = comments.next;
      },
      (err: Error) => {
        throw err;
      }
    );
  });

  async function submitComment() {
    let response: Result<Comment> = await $session.user.post(endpoint, {
      content: comment,
    });
    match(
      response,
      (newObj: Comment) => (comment_list = [...comment_list, newObj]),
      (err: Error) => {
        throw err;
      }
    );
    comment = "";
  }

  async function handleDelete(id) {
    const res = await $session.user.delete_(`comment/delete/${id}`);
    match(
      res,
      (_) => (comment_list = comment_list.filter((cmt) => cmt.id !== id)),
      (err: Error) => {
        throw err;
      }
    );
    deleteTarget = null;
  }

  async function handleLoadMore(url: string) {
    const { searchParams } = new URL(url);
    const page = parseInt(searchParams.get("page"));

    const res = await paginated_get(endpoint, {}, page);
    match(
      res,
      (comments: Paginated<Comment>) => {
        comment_list = [...comment_list, ...comments.results];
        next = comments.next;
      },
      (err: Error) => {
        throw err;
      }
    );
  }
</script>

<style>
  h3 {
    margin: 19px 0 -15px 0;
  }
</style>

{#if error}
  <UIError data={error} />
{/if}

{#if $session.user}
  <br />
  <h3>Add a comment</h3>
  <br />
  <textarea type="text" bind:value={comment} />
  <br />
  <button class="big" type="submit" on:click={submitComment}>SUBMIT</button>
{:else}
  <p>You must log in to comment</p>
{/if}

{#if deleteTarget}
  <Modal>
    Confirm delete
    <button
      style="margin-bottom: 5px"
      on:click={() => (deleteTarget = null)}>CANCEL</button>
    <button class="danger" on:click={() => handleDelete(deleteTarget)}>
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
  </Modal>
{/if}

{#await comment_promise}
  Loading...
{:then _}
  {#each comment_tree.roots as cmt (cmt.data.id)}
    <UIComment
      data={cmt.data}
      children={cmt.children}
      {post_id}
      on:delete={(event) => (deleteTarget = event.detail.id)}
      on:reply={(event) => (comment_list = [...comment_list, event.detail.comment])}
      on:error={(event) => (error = event.detail.error)} />

    <br />
  {/each}
  {#if next}
    <button on:click={() => handleLoadMore(next)}>Load More</button>
  {/if}
{/await}
