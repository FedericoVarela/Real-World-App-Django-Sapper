<script context="module" lang="ts">
  import type { AxiosResponse } from "axios"

  import { get } from "../../api";
  import { match } from "../../utils"
  import type { Post } from "../../types"

  export async function preload({ params }, _) {
    const { id } = params;

    //TODO: caching
    // async function get_or_fetch(id) {
    //     if (session.postCache.has(id)) {
    //         return {data: session.postCache.get(id)}
    //     } else {
    //         const data = await get(this.fetch, `blog/posts/${id}`)
    //         session.postCache.set(data.id, data)
    //         console.log(session.postCache)
    //         return { data }
    //     }
    // }

    // if (session.postCache) {
    //     return get_or_fetch(id)
    // } else {
    //     session.postCache = new Map()
    //     const data = get_or_fetch(id)
    //     console.log(session.postCache)

    //     return { data }
    // }

    const res = await get<Post>(`blog/posts/${id}`);
    return match(
      res,
      (post: AxiosResponse<Post>) => post,
      (err) => {throw err},
    )
  }
</script>

<script lang="ts" >
  import { stores, goto } from "@sapper/app";

  import type { Comment } from "../../types"

  export let data;
  const { id, title, content, author, tag } = data;
  const { session } = stores();
  const endpoint = `blog/posts/${id}/related`;

  let comment;
  let comment_list = [];

  let isAuthor = $session.user !== undefined && $session.user.username === author.username

  const comment_promise = get<Comment[]>(endpoint).then((data) => {
    match(
      data,
      (comments: AxiosResponse<Comment[]>) => comment_list = [...comment_list, ...comments.data],
      (err) => { throw err },
    )
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

  async function handleDelete() {
    $session.user.delete_(`blog/posts/${id}`)
    goto("/")
  }
</script>

<h1>{title}</h1>
{#if tag}<span>{tag.name}</span> <br />{/if}
<em>By {author.username}</em>
<p>{content}</p>

{#if isAuthor }
    <a href={`posts/update/${id}`}>UPDATE</a>
    <button on:click={handleDelete} >DELETE</button>
{/if}

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
