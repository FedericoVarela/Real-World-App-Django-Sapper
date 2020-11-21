<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import type { Post, Paginated } from "../types";
    import UIPost from "./Post.svelte";
    import PaginationControls from "./PaginationControls.svelte";

    export let data: Paginated<Post>;
    const dispatch = createEventDispatcher();

    function forward(event) {
        dispatch("change", event.detail);
    }
</script>

{#if data.results.length}
    {#each data.results as post}
        <UIPost data={post} />
    {/each}

    <PaginationControls
        previous={data.previous}
        next={data.next}
        on:change={forward} />
{:else}No posts here...{/if}
