<script lang="ts">
    import type { Post } from "../types";
    import FavoriteButton from "./FavoriteButton.svelte";

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
</script>

<a href={`posts/${id}`}>
    <h2>{title}</h2>
</a>
<em>By <a href={'profile/' + author.username}>{author.username}</a></em>
<br />
{#each tags as tag}({tag.name}) &ensp;{/each}
<FavoriteButton {id} {is_favorite} {favorite_count} />
<p>{content.substring(0, 50)}{content.length > 50 ? '...' : ''}</p>
