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

	const deleteIcon = `
	<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
	<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
	<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4L4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
	</svg>
	`;
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
		<button
			style="margin-bottom: 5px"
			on:click={() => (isAttemptingDelete = false)}>CANCEL</button>
		<button class="danger" on:click={handleDelete}>
			{@html deleteIcon}
			DELETE</button>
	</Modal>
{/if}

{#if isAuthor}
	<a class="button" href={`posts/update/${id}`}>
		<svg
			xmlns="http://www.w3.org/2000/svg"
			width="16"
			height="16"
			fill="currentColor"
			class="bi bi-pencil"
			viewBox="0 0 16 16">
			<path
				d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5L13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175l-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z" />
		</svg>
		UPDATE</a>
	<button class="danger" on:click={() => (isAttemptingDelete = true)}>
		{@html deleteIcon}
		DELETE</button>
{/if}
<CommentSection post_id={id} />
