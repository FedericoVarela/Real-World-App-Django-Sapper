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

{#if error}
  <UIError data={error} />
{/if}

{#if $session.user}
  <label for="comment">Comment something</label>
  <input type="text" bind:value={comment} />
  <button type="submit" on:click={submitComment}>SUBMIT</button>
{:else}
  <p>You must log in to comment</p>
{/if}

{#if deleteTarget}
  <Modal>
    Confirm delete
    <button on:click={() => (deleteTarget = null)}>CANCEL</button>
    <button on:click={() => handleDelete(deleteTarget)}>DELETE</button>
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
