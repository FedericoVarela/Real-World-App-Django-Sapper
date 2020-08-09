<script>
    export let data;
    const { title, content, author, tag } = data
</script>

<h2>{title}</h2>
{#if tag}
    <span>{tag.name}</span> <br>
{/if}
<em>By {author.username}</em>
<p>{content}</p>