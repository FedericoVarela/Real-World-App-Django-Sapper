<script context="module" lang="ts">
  import { get } from "../../../api";
  import { match } from "../../../utils";
  import type { Post } from "../../../types";

  export async function preload({ params }, session) {
    if (session.user === undefined) {
      return this.redirect(302, "user/login");
    } else {
      const { id } = params;
      const res = await get<Post>(`posts/${id}`);

      return match(
        res,
        (post: Post) => post,
        (_: Error) => {
          this.error(404, "Not found");
        }
      );
    }
  }
</script>

<script lang="ts">
  import { stores, goto } from "@sapper/app";

  import type { Tag } from "../../../types";
  import PostForm from "../../../components/PostForm.svelte";
  import UIError from "../../../components/Error.svelte";

  export let id: number;
  export let title: string;
  export let content: string;
  export let tags: Tag[];

  const { session } = stores();
  let error;
  const initial = {
    title,
    content,
    tags,
  };

  async function handleSubmit(event) {
    const { data } = event.detail;
    const res = await $session.user.patch(`posts/${id}`, data);
    match(
      res,
      (_) => goto(`posts/${id}`),
      (err: Error) => (error = err)
    );
  }
</script>

<h1>Update Post</h1>

{#if error}
  <UIError data={error} />
{/if}
<PostForm data={initial} on:submit={handleSubmit} />
