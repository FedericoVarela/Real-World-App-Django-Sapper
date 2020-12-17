<script lang="ts">
  import { stores } from "@sapper/app";

  import { match } from "../utils";
  import { paginated_get } from "../api";
  import type { Comment, Paginated, Result, Option } from "../types";

  import CommentComp from "./Comment.svelte";
  import Modal from "./Modal.svelte";
  import UIError from "./Error.svelte"

  export let post_id: number;

  //TODO: replies

  const { session } = stores();
  const endpoint = `posts/${post_id}/comments`;
  let comment;
  let comment_list: Comment[] = [];
  let next: Option<string>;
  let error: Error;
  // Comment whose deletion is being confirmed, if any
  let deleteTarget: Option<number> = null;

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

  function handleDelete(id) {
    const res = $session.user.delete_(`comment/delete/${id}`);

    match(
      res,
      (_) => {
        const index = comment_list.findIndex((comment) => comment.id === id);
        comment_list.splice(index, 1);
        comment_list = [...comment_list];
      },
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
  {#each comment_list as cmt}
    <CommentComp
      data={cmt}
      on:delete={(event) => (deleteTarget = event.detail.id)} />
    <br />
  {/each}
  {#if next}
    <button on:click={() => handleLoadMore(next)}>Load More</button>
  {/if}
{/await}
