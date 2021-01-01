<script context="module" lang="ts">
	import { maybe_authorized_get } from "../../api";
	import { match } from "../../utils";
	import type { Post } from "../../types";

	export async function preload({ params }, session) {
		const { id } = params;
		const { user } = session;

		const res = await maybe_authorized_get<Post>(`posts/${id}`, user);
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
	import { Remarkable } from "remarkable";

	import CommentSection from "../../components/CommentSection.svelte";
	import FavoriteButton from "../../components/FavoriteButton.svelte";
	import UIError from "../../components/Error.svelte";
	import Modal from "../../components/Modal.svelte";
	import Tag from "../../components/Tag.svelte";

	export let data: Post;
	const {
		id,
		title,
		content,
		author,
		tags,
		is_favorite,
		favorite_count,
		created_at,
	} = data;
	const { session } = stores();
	const markdown = new Remarkable();
	let isAttemptingDelete = false;
	let error: Error;

	$: isAuthor =
		$session.user !== undefined &&
		$session.user.username === author.username;

	async function handleDelete() {
		const res = await $session.user.delete_(`posts/${id}`);
		match(
			res,
			async () => await goto("/"),
			(err: Error) => (error = err)
		);
	}
</script>

<style>
	section {
		display: flex;
		justify-content: space-between;
		margin-top: 2em;
		color: var(--main);
		font-weight: 500;
	}

	a {
		max-width: 50%;
	}
</style>

<h1>{title}</h1>
{#each tags as tag}
	<Tag name={tag.name} />
{/each}

<section>
	<em>By
		<a href={'profile/' + author.username}>{author.username}</a>
		at
		{new Date(created_at).toUTCString()}</em>
	<FavoriteButton {id} {is_favorite} {favorite_count} />
</section>

{#if error}
	<UIError data={error} />
{/if}
{@html markdown.render(content)}

{#if isAttemptingDelete}
	<Modal>
		Confirm deletion
		<button style="margin-bottom: 5px" on:click={() => (isAttemptingDelete = false)}>CANCEL</button>
		<button class="danger" on:click={handleDelete}>DELETE</button>
	</Modal>
{/if}

{#if isAuthor}
	<a class="button" href={`posts/update/${id}`}>UPDATE</a>
	<button class="danger" on:click={() => (isAttemptingDelete = true)}>DELETE</button>
{/if}
<CommentSection post_id={id} />
