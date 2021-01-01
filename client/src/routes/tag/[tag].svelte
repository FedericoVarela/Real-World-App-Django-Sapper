<script lang="ts" context="module">
    export async function preload({ params }, _) {
        const { tag } = params;
        return { tag };
    }
</script>

<script lang="ts">
    import { paginated_get } from "../../api";
    import type { Paginated, Post } from "../../types";
    import { match } from "../../utils";
    import PostList from "../../components/PostList.svelte";
    import UIError from "../../components/Error.svelte";
    
    export let tag: string;

    async function getByTag(page: number) {
        const res = await paginated_get<Post>(`search/by-tag/${tag}`, {}, page);
        return match(
            res,
            (posts: Paginated<Post>) => posts,
            (err: Error) => {
                throw err;
            }
        );
    }

    let promise = getByTag(1);

    async function handleChangePage(event) {
        const { page } = event.detail
        promise = getByTag(page)
    }
</script>
<h1>{tag}</h1>
{#await promise}
    Loading...
{:then data}
    <PostList {data} on:change={handleChangePage}/>
{:catch err}
    <UIError data={err}/>
{/await}
