<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type { Option } from "../types";

    export let previous: Option<string> = null;
    export let next: Option<string> = null;

    const dispatch = createEventDispatcher()

    function changePage(url: string) {
        const path = new URL(url)
        dispatch("change", {
            endpoint: path.pathname.replace("/api/v0/", "").slice(0, -1),
            page: path.searchParams.get("page")
            
        })
    }

</script>

{#if previous}<button on:click={() => changePage(previous)} > &lt;&lt; </button>{/if}
{#if next}<button on:click={() => changePage(next)} > &gt;&gt; </button>{/if}
