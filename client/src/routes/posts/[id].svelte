<script context="module">
  import { get } from "../../api.ts";
  export async function preload({ params }, session) {
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

    const data = await get(this.fetch, `blog/posts/${id}`);
    return { data: data.data };
  }
</script>

<script>
  import { stores } from "@sapper/app";
  import { post } from "../../api.ts";

  export let data;
  const { id, title, content, author, tag } = data;
  const { session } = stores();
  const endpoint = `blog/posts/${id}/related`;

  let comment;
  let comment_list = [];

  const comment_promise = get(fetch, endpoint).then((data) => {
    comment_list = [...comment_list, ...data.data];
  });

  function submitComment(event) {
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

<h1>{title}</h1>
{#if tag}<span>{tag.name}</span> <br />{/if}
<em>By {author.username}</em>
<p>{content}</p>

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
