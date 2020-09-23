<script context="module" lang="ts">
  import type { AxiosResponse } from "axios";

  import { get } from "../../../api";
  import { match } from "../../../utils";
  import type { Post } from "../../../types";

  export async function preload({ params }, session) {
    if (session.user === undefined) {
      console.log(session.user);
      return this.redirect(302, "auth/login");
    } else {
      const { id } = params;
      const res = await get<Post>(`blog/posts/${id}`);

      return match(
        res,
        (post: AxiosResponse<Post>) => post.data,
        (err) => { throw err }
      );
    }
  }
</script>

<script lang="ts" >
  import { stores, goto } from "@sapper/app";

  export let id : number;
  export let title : string;
  export let content : string;

  const { session } = stores();

  let formData = {
    title: title,
    content: content,
  };

  async function handleSubmit() {
    const res = await $session.user.patch(`blog/posts/${id}`, formData);
    match(
      res,
      (_) => goto(`posts/${id}`),
      (_) => goto("posts")
    );
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <h1><input type="text" bind:value={formData.title} /></h1>
  <input type="text" bind:value={formData.content} />
  <button type="submit">UPDATE</button>
</form>
