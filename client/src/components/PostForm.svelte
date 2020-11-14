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

<form on:submit|preventDefault={handleSubmit}>
    <h1>
        <label for="title">Title</label>
        <input type="text" bind:value={data.title} />
    </h1>

    <label for="content" />
    <input type="text" bind:value={data.content} />

    <label for="tags" />
    <input type="text" bind:value={tags_input} />
    <button type="submit">SUBMIT</button>
</form>
