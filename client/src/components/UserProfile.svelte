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
        margin-right: 0.5em;
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

    hr,
    b {
        color: var(--main);
    }
</style>

<img id="pfp" src={picture} alt={`${username}'s profile picture`} />
<h1>{username}</h1>

<!-- Controls -->
{#if $session.user}
    {#if $session.user.username === username}
        <b>Edit</b>
        <hr />
        <div>
            <a class="button" href="user/edit">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-gear"
                    viewBox="0 0 16 16">
                    <path
                        d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z" />
                    <path
                        d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z" />
                </svg>
                Edit Profile</a>
            <a class="button" href="user/change-password">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-lock"
                    viewBox="0 0 16 16">
                    <path
                        d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2zM5 8h6a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z" />
                </svg>
                Change Password</a>
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
