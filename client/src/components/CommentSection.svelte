<script lang="ts">
  import { stores } from "@sapper/app";

  import { match } from "../utils";
  import { paginated_get } from "../api";
  import CommentComp from "./Comment.svelte"
  import type { Comment, Paginated, Result } from "../types";

  export let post_id: number;

  const { session } = stores();
  const endpoint = `posts/${post_id}/comments`;
  let comment;
  let comment_list : Comment[] = [];

  const comment_promise = paginated_get<Comment>(endpoint).then((data) => {
    match(
      data,
      (comments: Paginated<Comment>) => (comment_list = [...comment_list, ...comments.results]),
      (err) => {
        throw err;
      }
    );
  });

  async function submitComment() {
    let response : Result<Comment> = await $session.user.post(endpoint, {
      content: comment,
    });
    match(
      response,
      (newObj: Comment) => comment_list = [...comment_list, newObj],
      (err: Error)   => { throw err }
    )
    comment = "";
  }

  function handleDelete(event) {
    // TODO: Confirm deletion
    const id = event.detail.id
    const index = comment_list.findIndex((comment) => comment.id === id)
    comment_list.splice(index, 1)
    comment_list = [...comment_list]
  }

</script>

{#if $session.user}
  <label for="comment">Comment something</label>
  <input type="text" bind:value={comment} />
  <button type="submit" on:click={submitComment}>SUBMIT</button>
{:else}
  <p>You must log in to comment</p>
{/if}

{#await comment_promise}
  Loading...
{:then _}
  {#each comment_list as cmt}
    <CommentComp data={cmt} on:delete={handleDelete} />
    <br>
  {/each}
{/await}
