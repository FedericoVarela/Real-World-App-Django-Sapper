<script lang="ts">
  import { paginated_get } from "../api";
  import { match } from "../utils";
  import type { Post, Paginated } from "../types";

  import PostComponent from "../components/Post.svelte";
  import ErrorComponent from "../components/Error.svelte";
  import TagList from "../components/TagList.svelte";
  import PaginationControls from "../components/PaginationControls.svelte";

  async function getFeed(page: number): Promise<Paginated<Post>> {
    const res = await paginated_get<Post>("posts", {}, page);
    return match(
      res,
      (posts: Paginated<Post>) => posts,
      (err: Error) => {
        throw err;
      }
    );
  }

  let promise = getFeed(1);

  async function handleChangePage(event) {
    const { page } = event.detail;
    promise = getFeed(page)
  }
</script>

<style>
  h1 {
    text-align: center;
    margin: 0 auto;
  }

  h1 {
    color: rgb(255, 62, 0);
    font-size: 2.8em;
    text-transform: uppercase;
    font-weight: 700;
    margin: 0 0 0.5em 0;
  }

  @media (min-width: 480px) {
    h1 {
      font-size: 4em;
    }
  }
</style>

<svelte:head>
  <title>Sapper project template</title>
</svelte:head>

<h1>Real World App: Django + Sapper</h1>

<a href="posts/create">Post something</a>

<TagList />

{#await promise}
  Loading...
{:then posts}
  {#each posts.results as post}
    <PostComponent data={post} />
  {/each}
  <PaginationControls
    previous={posts.previous}
    next={posts.next}
    on:change={handleChangePage} />
{:catch err}
  <ErrorComponent data={err} />
{/await}
