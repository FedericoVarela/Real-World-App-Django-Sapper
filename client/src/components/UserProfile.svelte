<script lang="ts">
    import { stores } from "@sapper/app";
    import type { Profile, Post, Paginated } from "../types";
    import { maybe_authorized_paginated_get } from "../api";
    import { match } from "../utils";
    import UIError from "./Error.svelte";
    import PostList from "./PostList.svelte";
    import FollowButton from "./FollowButton.svelte";

    export let data: Profile;
    const { session } = stores();
    const { username, picture, description, is_following } = data;

    enum ActiveTab {
        MyPosts,
        Favorites,
    }
    let active = ActiveTab.MyPosts;

    async function getPostsFromEndpoint(endpoint: string, page: number) {
        const res = await maybe_authorized_paginated_get<Post>(
            endpoint,
            $session.user,
            page
        );
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
    button:not(.tab),
    a.button {
        margin-bottom: 10px;
        margin-right: .5em;
    }

    button.tab {
        background-color: transparent;
        color: var(--main);
        border-radius: 0;
    }

    button.tab.active {
        border-bottom: var(--main) solid 4px;
    }

    img#pfp {
        border-radius: 100%;
        max-width: 250px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    div {
        display: flex;
        justify-content: flex-start;
    }

    hr, b {
        color: var(--main)
    }
</style>

<img id="pfp" src={picture} alt={`${username}'s profile picture`} />
<h1>{username}</h1>

<!-- Controls -->
{#if $session.user}
    {#if $session.user.username === username}
        <b>Edit</b>
        <hr>
        <div>
            <a class="button" href="user/edit">Edit Profile</a>
            <a class="button" href="user/change-password">Change Password</a>
        </div>
    {:else}
        <FollowButton {username} {is_following} />
    {/if}
    <br />
    <p>{description ? description : 'This user has no description'}</p>
{/if}

<button
    class="tab"
    class:active={active === ActiveTab.MyPosts}
    on:click={() => (promise = changeTab(ActiveTab.MyPosts))}>
    Posts</button>
<button
    class="tab"
    class:active={active === ActiveTab.Favorites}
    on:click={() => (promise = changeTab(ActiveTab.Favorites))}>
    Favorites</button>
<br />
<br />
{#await promise}
    Loading...
{:then posts}
    <PostList data={posts} on:change={handleChangePage} />
{:catch err}
    <UIError data={err} />
{/await}
