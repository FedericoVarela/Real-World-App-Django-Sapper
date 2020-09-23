<script context="module" lang="ts">
  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "auth/login");
    }
  }
</script>

<script lang="ts">
  import { stores, goto } from "@sapper/app";

  import { match } from "../../utils";
  import type { Post } from "../../types";
  // Import with different name to avoid collision with the Error class
  import ErrorComponent from "../../components/Error.svelte";

  const { session } = stores();
  const data = {
    title: "",
    content: "",
    draft: false,
  };

  let error : string;

  async function handleSubmit() {
    const res = await $session.user.post("blog/posts", data);
    // if ($session.postCache === undefined) {
    //   $session.postCache = new Map()
    // }
    // $session.postCache.set(res.id, res)
    match(
      res,
      (post : Post) => goto(`posts/${post.id}`),
      (err: Error) => error = err.message
    );
  }
</script>

<h1>New Article</h1>

{#if error}
  <ErrorComponent message={error} />
{/if}

<form on:submit|preventDefault={handleSubmit}>
  <label for="title">Title</label>
  <input class="input" type="text" bind:value={data.title} />

  <label for="content">Content</label>
  <textarea type="text" bind:value={data.content} />
  <input type="checkbox" bind:checked={data.draft} />

  <button type="submit">SUBMIT</button>
</form>
