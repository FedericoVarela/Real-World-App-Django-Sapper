<script lang="ts" >
    import type { Post } from "types"

    export let data : Post;
    const { id, title, content, author, tag } = data
</script>

<a href={`posts/${id}`}>
    <h2>{title}</h2>
</a>
{#if tag}
    <span>{tag.name}</span> <br>
{/if}
<em>By {author.username}</em>
<p>{content}</p>