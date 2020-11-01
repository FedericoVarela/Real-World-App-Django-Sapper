<script lang="ts">
  import { paginated_get } from "../api";
  import { match } from "../utils";
  import type { Post, Paginated } from "../types";
  import PostListItem from "../components/PostListItem.svelte";
  import ErrorComponent from "../components/Error.svelte";


  async function getFeed(): Promise<Paginated<Post>> {
    const res = await paginated_get<Post>("posts");
    return match(
      res,
      (posts: Paginated<Post>) => posts,
      (err: Error) => {
        throw err;
      }
    );
  }

  let promise = getFeed();

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

{#await promise}
  Loading...
{:then posts}
  {#each posts.results as post}
    <PostListItem data={post} />
  {/each}
  {#if posts.next}<button>Next</button>{/if}
{:catch err}
  <ErrorComponent data={err} />
{/await}
