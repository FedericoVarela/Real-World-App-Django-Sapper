<script lang="ts" context="module">
    export async function preload(page, session) {
        if (session.user === undefined) {
            return this.redirect(302, "user/login?next=user/feed");
        }
    }
</script>

<script lang="ts">
    import { stores } from "@sapper/app";
    import type { Post, Paginated } from "../../types";
    import { match } from "../../utils";
    import PostList from "../../components/PostList.svelte";
    import UIError from "../../components/Error.svelte";

    const { session } = stores();

    async function getFeed(page: number): Promise<Paginated<Post>> {
        const res = await $session.user.paginated_get("feed", page);
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
		promise = getFeed(page);
	}
</script>

<h1>My Feed</h1>

{#await promise}
    Loading...
{:then posts}
    <PostList data={posts} on:change={handleChangePage} />
{:catch err}
    <UIError data={err} />
{/await}
