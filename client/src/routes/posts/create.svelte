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
  import ErrorComponent from "../../components/Error.svelte";

  const { session } = stores();
  const data = {
    title: "",
    content: "",
  };

  let error: Error;

  async function handleSubmit() {
    const res = await $session.user.post("posts", data);
    match(
      res,
      (post: Post) => goto(`posts/${post.id}`),
      (err: Error) => (error = err)
    );
  }
</script>

<h1>New Article</h1>

{#if error}
  <ErrorComponent data={error} />
{/if}

<form on:submit|preventDefault={handleSubmit}>
  <label for="title">Title</label>
  <input class="input" type="text" bind:value={data.title} />

  <label for="content">Content</label>
  <textarea type="text" bind:value={data.content} />

  <button type="submit">SUBMIT</button>
</form>
