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
<a href="user/feed">My Feed</a>

<TagList />

{#await promise}
	Loading...
{:then posts}
	<PostList data={posts} on:change={handleChangePage} />
{:catch err}
	<UIError data={err} />
{/await}
