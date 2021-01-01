<script>
    export let name
</script>

<style>
    a {
        color: var(--main);
        background-color: var(--light);
        text-decoration: none;
        border-radius: 16px;
        margin: 2px 3px;
        padding: 4px 8px;
        white-space: nowrap;
        display: inline-block;
    }
</style>

<a href={"tag/"+name}>{name}</a>