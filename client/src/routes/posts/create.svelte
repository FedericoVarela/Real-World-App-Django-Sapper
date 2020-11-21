<script context="module" lang="ts">
  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "user/login");
    }
  }
</script>

<script lang="ts">
  import { stores, goto } from "@sapper/app";

  import { match } from "../../utils";
  import type { Post } from "../../types";
  import UIError from "../../components/Error.svelte";
  import PostForm from "../../components/PostForm.svelte";

  const { session } = stores();
  let error: Error;

  async function handleSubmit(event) {
    const { data } = event.detail
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
  <UIError data={error} />
{/if}
<PostForm on:submit={handleSubmit} />
