<script context="module" lang="ts">
  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "auth/login");
    }
  }
</script>

<script lang="ts">
  import { stores, goto } from "@sapper/app";
  import type { AxiosResponse } from "axios"

  import { post } from "../../api";
  import { match } from "../../utils";
  import type { Post } from "../../types";
  import Message from "../../components/Message.svelte"

  const { session } = stores();
  const data = {
    title: "",
    content: "",
    draft: false,
  };

  let error : string;

  async function handleSubmit() {
    const res = await post<Post>("blog/posts", data, {
      Authorization: `Bearer ${$session.user.access_token}`,
    });
    // if ($session.postCache === undefined) {
    //   $session.postCache = new Map()
    // }
    // $session.postCache.set(res.id, res)
      console.log(res)
    match(
      res,
      (post : AxiosResponse<Post>) => goto(`posts/${post.data.id}`),
      (err: Error) => error = err.message
    );
  }
</script>

<h1>New Article</h1>

{#if error}
  <Message msg={error} level="danger" />
{/if}

<form on:submit|preventDefault={handleSubmit}>
  <label for="title">Title</label>
  <input class="input" type="text" bind:value={data.title} />

  <label for="content">Content</label>
  <textarea type="text" bind:value={data.content} />
  <input type="checkbox" bind:checked={data.draft} />

  <button type="submit">SUBMIT</button>
</form>
