<script context="module" lang="ts">
  import { get } from "../../api";
  import { match } from "../../utils";
  import type { Post } from "../../types";

  export async function preload({ params }, _) {
    const { id } = params;

    const res = await get<Post>(`posts/${id}`);
    return match(
      res,
      (data: Post) => {
        return { data };
      },
      (_: Error) => {
        this.error(404, "Not found");
      }
    );
  }
</script>

<script lang="ts">
  import { stores, goto } from "@sapper/app";

  import CommentSection from "../../components/CommentSection.svelte";

  export let data: Post;
  const { id, title, content, author, tags } = data;
  const { session } = stores();

  let isAuthor =
    $session.user !== undefined && $session.user.username === author.username;

  async function handleDelete() {
    $session.user.delete_(`posts/${id}`);
    goto("/");
  }
</script>

<h1>{title}</h1>
<em>By {author.username}</em>
<br />
{#each tags as tag}({tag.name}) &ensp;{/each}
<p>{content}</p>

{#if isAuthor}
  <a href={`posts/update/${id}`}>UPDATE</a>
  <button on:click={handleDelete}>DELETE</button>
{/if}

<CommentSection post_id={id} />
