<script lang="ts">
    export let data: Error;
    let errorList;

    try {
        const fromAPI = Object.values(JSON.parse(data.message));
        errorList = fromAPI

    } catch (err) {
        errorList = [data.message]
    }

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
