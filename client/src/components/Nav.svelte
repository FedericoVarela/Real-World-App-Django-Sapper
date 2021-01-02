<script>
  import { fly } from "svelte/transition";
  import { onMount } from "svelte";
  import NavLinks from "./NavLinks.svelte";

  export let segment;
  // Tp avoid warning message
  segment;
  let overlay = false;

  onMount(function () {
    document.addEventListener("click", (e) => {
      console.log(e.target.tagName)
      if (!e.target.closest("aside") && !e.target.closest("#menu") || e.target.tagName === "A" || e.target.tagName === "BUTTON") {
        overlay = false;
      }
    });
  });
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

  button {
    background-color: transparent;
    color: inherit;
  }

  button {
    text-decoration: none;
    padding: 1em 0.5em;
    display: block;
  }

  #menu {
    display: none;
  }

  @media only screen and (max-width: 600px) {
    #menu {
      display: initial;
    }

    ul {
      display: none;
    }
  }

  aside {
    position: fixed;
    padding: 100px;
    background-color: white;
    color: var(--main);
    height: 100vh;
    z-index: 999;
    display: flex;
    flex-direction: column;
    right: 0;
  }
</style>

<nav>
  <ul>
    <NavLinks />
  </ul>
  <button id="menu" on:click={() => (overlay = !overlay)}>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="26"
      height="26"
      fill="currentColor"
      class="bi bi-three-dots-vertical"
      viewBox="0 0 16 16">
      <path
        d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0zm0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z" />
    </svg>
  </button>
</nav>

{#if overlay}
  <aside in:fly={{ x: 100, duration: 400 }}>
    <NavLinks />
  </aside>
{/if}
