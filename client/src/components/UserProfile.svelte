<script lang="ts">
    import { stores } from "@sapper/app";
    import type { Profile, Post, Paginated } from "../types";
    import { paginated_get } from "../api";
    import { match } from "../utils";
    import UIError from "./Error.svelte";
    import PostList from "./PostList.svelte";

    export let data: Profile;
    const { session } = stores();
    const { username, picture, description, created_at } = data;

    enum ActiveTab {
        MyPosts,
        Favorites,
    }
    let active = ActiveTab.MyPosts;

    async function getPostsFromEndpoint(endpoint: string, page: number) {
        const res = await paginated_get<Post>(endpoint, {}, page);
        return match(
            res,
            (posts: Paginated<Post>) => posts,
            (err: Error) => {
                throw err;
            }
        );
    }

    const getUsersPosts = (page: number) =>
        getPostsFromEndpoint(`search/by-author/${username}`, page);
    const getUserFavorites = (page: number) =>
        getPostsFromEndpoint(`favorites/${username}`, page);

    let promise = getUsersPosts(1);

    function changeTab(tab: ActiveTab, page = 1): Promise<Paginated<Post>> {
        active = tab;
        switch (tab) {
            case ActiveTab.MyPosts:
                return getUsersPosts(page);
            case ActiveTab.Favorites:
                return getUserFavorites(page);
        }
    }

    async function handleChangePage(event) {
        const { page } = event.detail;
        promise = changeTab(active, page);
    }
</script>

<style>
    button.active {
        background-color: rgb(255, 62, 0);
        color: white;
    }
</style>

<h1>{username}</h1>
<img src={picture} alt={`${username}'s profile picture`} />
<em>{created_at}</em>
<p>{description ? description : 'This user has no description'}</p>

<!-- Controls -->
{#if $session.user && $session.user.username === username}
    <a href="user/change-password">Change Password</a>
    <a href="user/edit">Edit Profile</a>
{/if}

<button
    class:active={active === ActiveTab.MyPosts}
    on:click={() => (promise = changeTab(ActiveTab.MyPosts))}>
    My Posts</button>
<button
    class:active={active === ActiveTab.Favorites}
    on:click={() => (promise = changeTab(ActiveTab.Favorites))}>
    My Favorites</button>

{#await promise}
    Loading...
{:then posts}
    <PostList data={posts} on:change={handleChangePage} />
{:catch err}
    <UIError data={err} />
{/await}
