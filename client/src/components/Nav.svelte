<script>
  import { stores } from "@sapper/app";
  const { session } = stores();

  export let segment;
  $: logged = $session.user !== undefined;


</script>

<style>
  nav {
    border-bottom: 1px solid rgba(255, 62, 0, 0.1);
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

  /* [aria-current] {
    position: relative;
    display: inline-block;
  }

  [aria-current]::after {
    position: absolute;
    content: "";
    width: calc(100% - 1em);
    height: 2px;
    background-color: rgb(255, 62, 0);
    display: block;
    bottom: -1px;
  } */

  a {
    text-decoration: none;
    padding: 1em 0.5em;
    display: block;
  }
</style>

<nav>
  <ul>
    <li>
      <a aria-current={segment === undefined ? 'page' : undefined} href=".">
        Home
      </a>
    </li>
    {#if logged}
      <li>
        <a
          aria-current={segment === 'auth' ? 'page' : undefined}
          href="auth/profile/">
          {$session.user.username}
        </a>
      </li>
      <li>
        <a
          aria-current={segment === 'posts' ? 'page' : undefined}
          href="posts/create">
          New Article
        </a>
      </li>
    {:else}
      <li>
        <a
          aria-current={segment === 'auth' ? 'page' : undefined}
          href="auth/login/">
          Log In
        </a>
        <a
          aria-current={segment === 'auth' ? 'page' : undefined}
          href="auth/signup/">
          Sign Up
        </a>
      </li>
    {/if}
  </ul>
</nav>
