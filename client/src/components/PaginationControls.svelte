<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type { Option } from "../types";

    export let previous: Option<string> = null;
    export let next: Option<string> = null;

    const dispatch = createEventDispatcher();

    function changePage(url: string) {
        const path = new URL(url);
        dispatch("change", {
            endpoint: path.pathname.replace("/api/v0/", "").slice(0, -1),
            page: path.searchParams.get("page"),
        });
    }
</script>

<style>
    button {
        margin: 10px 0;
        font-size: 170%;
    }
</style>

{#if previous}<button class="big" on:click={() => changePage(previous)}> &lt;</button>{/if}
{#if next}<button class="big" on:click={() => changePage(next)}> &gt; </button>{/if}
