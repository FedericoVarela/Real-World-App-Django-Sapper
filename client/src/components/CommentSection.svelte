<script lang="ts">
  import { stores } from "@sapper/app";
  import type { Comment, Author } from "../types";
  import { match } from "../utils"
  import { get } from "../api"

  export let post_id: number;
  export let author : Author;
  
  const { session } = stores();
  const endpoint = `blog/posts/${post_id}/related`
  let comment;
  let comment_list = [];

  let isAuthor =
    $session.user !== undefined && $session.user.username === author.username;

  const comment_promise = get<Comment[]>(endpoint).then((data) => {
    match(
      data,
      (comments: Comment[]) => (comment_list = [...comment_list, ...comments]),
      (err) => {
        throw err;
      }
    );
  });

  function submitComment() {
    let response = $session.user.post(endpoint, {
      content: comment,
    });
    const newObj = {
      content: comment,
      created_at: new Date(),
      author: $session.user.username,
    };
    comment_list = [...comment_list, newObj];
    comment = "";
    return response;
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
    <p>{cmt.content}</p>
    <em>{new Date(cmt.created_at)}</em>
  {/each}
{/await}