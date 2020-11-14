<script lang="ts" >
    import type { Post } from "../types"

    export let data : Post;
    const { id, title, content, author, tags } = data
</script>

<a href={`posts/${id}`}>
    <h2>{title}</h2>
</a>
<em>By {author.username}</em> <br>
{#each tags as tag}
    ({tag.name}) &ensp;
{/each}
<p>{content}</p>