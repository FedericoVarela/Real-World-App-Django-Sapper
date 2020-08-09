<script>
  import axios from "axios"

  import { get } from "../api"
  import PostListItem from "../components/PostListItem.svelte"

  async function getFeed() {
    return get(fetch, "blog/posts")
  }

  let promise = getFeed().catch(err => err);
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
{#await promise}
  Loading...
{:then posts}
  {#each posts as post}
    <PostListItem data={post} />
  {/each}
{:catch error}
    <p>Oops! There has been an error</p>
{/await}
