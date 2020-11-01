<script lang="ts">
    export let data: Error;

    const errorList = Object.values(JSON.parse(data.message));

</script>

<style>
    div {
        color: red;
    }
</style>

<div>
    {#each errorList as err }
        {err}
    {/each}
</div>
