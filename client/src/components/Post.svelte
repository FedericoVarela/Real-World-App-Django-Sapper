<script lang="ts">
    import type { Post } from "../types";
    import FavoriteButton from "./FavoriteButton.svelte";
    import Tag from "./Tag.svelte";

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

<style>
    article {
        box-shadow: 0 2px 9px 0 rgba(0, 0, 0, 0.25);
        border-radius: 15px;
        padding: 12px 20px;
        margin-top: 17px;
    }

    div {
        float: right;
    }
</style>

<article>
    <a href={`posts/${id}`}>
        <h2>{title}</h2>
    </a>
    <em>By <a href={'profile/' + author.username}>{author.username}</a></em>
    <br />
    <p>{content.substring(0, 50)}{content.length > 50 ? '...' : ''}</p>
    <div>
        {#each tags as tag}
            <Tag name={tag.name} />
            &ensp;
        {/each}
    </div>
    <FavoriteButton {id} {is_favorite} {favorite_count} />
</article>
