<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let data = {
        title: "",
        content: "",
        tags: [],
    };

    const dispatch = createEventDispatcher();

    // Set to initial value joined
    let tags_input = data.tags.map(({ name }) => name).join(",");
    $: data.tags = tags_input.split(",");

    function handleSubmit() {
        dispatch("submit", {
            data,
        });
    }
</script>

<style>
    label {
        margin-top: 10px;
    }

    textarea {
        height: 30vh;
    }
</style>

<form on:submit|preventDefault={handleSubmit}>
    <label for="title">Title</label>
    <input type="text" bind:value={data.title} />

    <label for="content">Content</label>
    <textarea type="text" bind:value={data.content} />

    <label for="tags">Tags (separated by commas)</label>
    <input type="text" bind:value={tags_input} />
    <button type="submit">SUBMIT</button>
</form>
