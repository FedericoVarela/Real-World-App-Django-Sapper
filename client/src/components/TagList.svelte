<script lang="ts">
    import { paginated_get } from "../api";
    import type { Paginated, Tag } from "../types";
    import { match } from "../utils";
    import UIError from "./Error.svelte";
    import PaginationControls from "./PaginationControls.svelte";

    async function load(page: number): Promise<Paginated<Tag>> {
        return match(
            await paginated_get("tags", {}, page),
            (tags: Tag[]) => tags,
            (err: Error) => {
                throw err;
            }
        );
    }

    let promise = load(1);

    //TODO: page size
    async function handleChangePage(event) {
        const { page } = event.detail;
        promise = load(page);
    }
</script>

{#await promise}
    Loading...
{:then tags}
    {#each tags.results as tag}
        <a href={'tag/' + tag.name}>{tag.name}</a>
        <br />
    {/each}
    <PaginationControls
        previous={tags.previous}
        next={tags.next}
        on:change={handleChangePage} />
{:catch err}
    <UIError data={err} />
{/await}
