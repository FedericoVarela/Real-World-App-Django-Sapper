<script>
  import { stores } from "@sapper/app";
  const { session } = stores();

  export let segment;
  // Tp avoid warning message
  segment;
  $: logged = $session.user !== undefined && $session.user !== null;
</script>

<style>
  nav {
    border-bottom: 1px solid rgba(255, 62, 0, 0.1);
    color: var(--light);
    background-color: var(--dark);
    font-weight: 300;
    padding: 0 1em;
    display: flex;
    justify-content: flex-end;
  }

  ul {
    margin: 0;
    padding: 0;
  }

  /* clearfix */
  ul::after {
    content: "";
    display: block;
    clear: both;
  }

  li {
    display: block;
    float: left;
  }

  a {
    text-decoration: none;
    padding: 1em 0.5em;
    display: block;
  }
</style>

<nav>
  <ul>
    <li><a href="."> Home </a></li>

    {#if logged}
      <!---------------------------------------------------- -->
      <li><a href="user/profile/"> {$session.user.username} </a></li>
      <li><a href="posts/create"> New Article </a></li>
      <li><a href="user/feed">My Feed</a></li>
    {:else}
      <!-- ------------------------------------------------------ -->
      <li>  <a href="user/login/"> Log In </a></li>
      <li><a href="user/signup/"> Sign Up </a></li>
    {/if}
  </ul>
</nav>
