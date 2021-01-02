<script>
    import { stores } from "@sapper/app";

    const { session } = stores();

    $: logged = $session.user !== undefined && $session.user !== null;

    function logout() {
        $session.user = undefined;
        localStorage.removeItem("username");
        localStorage.removeItem("refresh");
    }
</script>

<style>
    li {
        display: block;
        float: left;
    }

    a,
    button {
        text-decoration: none;
        padding: 1em 0.5em;
        display: block;
        background-color: transparent;
        color: inherit;
        font-weight: 300;

    }
</style>

<li><a href="."> Home </a></li>
{#if logged}
    <!---------------------------------------------------- -->
    <li><a href="user/profile/"> {$session.user.username} </a></li>
    <li><a href="posts/create"> New Article </a></li>
    <li><a href="user/feed">My Feed</a></li>
    <li><button on:click={logout}>Logout</button></li>
{:else}
    <!-- ------------------------------------------------------ -->
    <li><a href="user/login/"> Log In </a></li>
    <li><a href="user/signup/"> Sign Up </a></li>
{/if}
