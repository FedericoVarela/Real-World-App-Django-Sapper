<script lang="ts">
  import type { AxiosResponse } from "axios";

  import { get } from "../api";
  import { match } from "../utils";
  import type { Post } from "../types";
  import PostListItem from "../components/PostListItem.svelte";

  // const { session } = stores()

  async function getFeed() : Promise<Post[]> {
    const res = await get<Post[]>("blog/posts");
    // if ($session.postCache === undefined) {
    //   $session.postCache = new Map()
    // }

    // res.data.forEach( e => {
    //   //TODO: remove id from the stored object as it's redundant
    //   $session.postCache.set(e.id, e)
    // });

    // console.log($session.postCache)

    return match(
      res,
      (posts: AxiosResponse<Post[]>) => posts.data,
      (err) => {throw err}
    );
  }

  let promise = getFeed().catch((err) => err);

  //TODO: testing
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
  {#each posts as post}
    <PostListItem data={post} />
  {/each}
{:catch _}
  <p>Oops! There has been an error</p>
{/await}
