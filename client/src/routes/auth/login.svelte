<!-- <script context="module">
  export function preload(page, session) {

  }
</script> -->

<script>
  import { goto, stores } from "@sapper/app";
  import { User, post } from "../../api";
import Error from "../_error.svelte";

  const { session } = stores();

  let username;
  let password;
  let promise;

  const logIn = async () => {
    const res = await post("jwt/create", {
      username,
      password,
    });
    $session.user = new User(res);
    goto("auth/profile");
  };

  const handleAuth = () => promise = logIn()

</script>

<style>
  form {
    display: flex;
    flex-direction: column;
  }

  form > input,
  button {
    margin: 15px 2rem;
    float: left;
  }
</style>

  <h1>Log In</h1>
  {#if promise !== undefined}
    {#await promise}
      Logging in...
    {:then  _ } 
      <br>
    {:catch error}
      {#if error.message.includes("401")}
        Incorrect username or password
      {:else}
        Oops! Something went wrong
      {/if}
    {/await}
  {/if}

  <form on:submit|preventDefault={handleAuth}>
    <label for="username">Username</label>
    <input type="text" bind:value={username} required />
    <label for="password">Password</label>
    <input type="password" bind:value={password} required />
    <button type="submit">LOG IN</button>
  </form>

