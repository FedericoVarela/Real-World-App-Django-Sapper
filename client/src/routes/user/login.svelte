<script lang="ts">
  import { goto, stores } from "@sapper/app";
  import { User } from "../../api";
  import { match } from "../../utils";
  import UIError from "../../components/Error.svelte";

  const { session } = stores();

  let username;
  let password;
  let promise;

  async function handleLogin() {
    const res = await User.login(username, password);
    return match(
      res,
      (user: User) => {        
        $session.user = user;
        goto("user/profile");
      },
      (err: Error) => {
        throw err;
      }
    );
  }

  const handleAuth = () => (promise = handleLogin());
</script>

<style>
  button {
    margin: 15px 0;
    float: left;
    padding: 10px;
    border-radius: 10px;
  }

  label {
    color: var(--main)
  }
</style>

<h1>Log In</h1>
{#if promise !== undefined}
  {#await promise}
    Logging in...
  {:then _}
    <br />
  {:catch error}
    <UIError data={error} />
  {/await}
{/if}

<form on:submit|preventDefault={handleAuth}>
  <label for="username">Username</label>
  <input type="text" class="input" bind:value={username} required />
  <label for="password">Password</label>
  <input type="password" bind:value={password} required />
  <button type="submit">LOG IN</button>
</form>

Don't have an account? <a href="user/signup" class="accentuated">Create one</a>