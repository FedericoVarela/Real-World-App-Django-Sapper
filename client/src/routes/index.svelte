<script lang="ts">
	import { stores } from "@sapper/app";
	import { maybe_authorized_paginated_get } from "../api";
	import { match } from "../utils";
	import type { Post, Paginated } from "../types";

	import UIError from "../components/Error.svelte";
	import TagList from "../components/TagList.svelte";
	import PostList from "../components/PostList.svelte";

	const { session } = stores();
	
	async function getPosts(page: number): Promise<Paginated<Post>> {
		const res = await maybe_authorized_paginated_get<Post>(
			"posts",
			$session.user,
			page
		);
		return match(
			res,
			(posts: Paginated<Post>) => posts,
			(err: Error) => {
				throw err;
			}
		);
	}

	let promise = getPosts(1);

	async function handleChangePage(event) {
		const { page } = event.detail;
		promise = getPosts(page);
	}
</script>

<style>
	h1 {
		text-align: center;
		margin: 0 auto;
		font-size: 2.8em;
		text-transform: uppercase;
		font-weight: 700;
		margin: 0 0 0.5em 0;
	}
</style>

<svelte:head>
	<title>Real World App: Django + Sapper</title>
</svelte:head>

<h1>Global Feed</h1>

<TagList />

{#await promise}
	Loading...
{:then posts}
	<PostList data={posts} on:change={handleChangePage} />
{:catch err}
	<UIError data={err} />
{/await}
