<script lang="ts" >
  import { goto, stores } from "@sapper/app";
  import { User, post } from "../../api.ts";
  import Error from "../_error.svelte";

  const { session } = stores();

  let username;
  let password;
  let promise;

  async function handleLogin() {
    $session.user = await User.login(username, password)
    goto("auth/profile");
  };

  const handleAuth = () => promise = handleLogin()

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
        <!-- Oops! Something went wrong -->
        {error}
      {/if}
    {/await}
  {/if}

  <form on:submit|preventDefault={handleAuth}>
    <label for="username">Username</label>
    <input type="text" class="input" bind:value={username} required />
    <label for="password">Password</label>
    <input type="password" bind:value={password} required />
    <button type="submit">LOG IN</button>
  </form>

