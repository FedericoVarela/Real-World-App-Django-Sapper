<script lang="ts">
    import { paginated_get } from "../api";
    import type { Paginated, Tag } from "../types";
    import { match } from "../utils";

    import UIError from "./Error.svelte";
    import PaginationControls from "./PaginationControls.svelte";
    import UITag from "./Tag.svelte";

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

    async function handleChangePage(event) {
        const { page } = event.detail;
        promise = load(page);
    }
</script>

<style>
    div {
        max-width: 80vw;
    }
</style>

All tags
<hr>
{#await promise}
    Loading...
{:then tags}
    <div>
        {#each tags.results as tag}
            <UITag name={tag.name} />
        {/each}
        <br>
        <PaginationControls
            previous={tags.previous}
            next={tags.next}
            on:change={handleChangePage} />
    </div>
{:catch err}
    <UIError data={err} />
{/await}
