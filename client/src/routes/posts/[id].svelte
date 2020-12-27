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
	import Modal from "../../components/Modal.svelte"

	export let data: Post;
	const {
		id,
		title,
		content,
		author,
		tags,
		is_favorite,
		favorite_count,
	} = data;
	const { session } = stores();
	const markdown = new Remarkable();
	let isAttemptingDelete = false;
	let error: Error;

	let isAuthor =
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

<h1>{title}</h1>
<em>By <a href={'profile/' + author.username}>{author.username}</a> </em>
<br />
{#each tags as tag}({tag.name}) &ensp;{/each}

{#if error}
	<UIError data={error} />
{/if}
{@html markdown.render(content)}

<FavoriteButton {id} {is_favorite} {favorite_count} />

{#if isAttemptingDelete}
	<Modal>
		Confirm deletion
		<button on:click={() => isAttemptingDelete = false} >CANCEL</button>
		<button on:click={handleDelete}>DELETE</button>
	</Modal>
{/if}

{#if isAuthor}
	<a href={`posts/update/${id}`}>UPDATE</a>
	<button on:click={() => (isAttemptingDelete = true)}>DELETE</button>
{/if}
<CommentSection post_id={id} />
