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
        padding: 0px 10px;
    }

    button > svg {
        transform: translateY(-19%);
    }
</style>

{#if previous}
    <button class="big" on:click={() => changePage(previous)}>
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-arrow-left"
            viewBox="0 0 16 16">
            <path
                fill-rule="evenodd"
                d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z" />
        </svg></button>
{/if}
{#if next}
    <button class="big" on:click={() => changePage(next)}>
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-arrow-right"
            viewBox="0 0 16 16">
            <path
                fill-rule="evenodd"
                d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z" />
        </svg>
    </button>
{/if}
