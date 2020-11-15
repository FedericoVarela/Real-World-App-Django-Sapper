<script lang="ts">
  import { goto, stores } from "@sapper/app";
  import { User } from "../../api";
  import UIError from "../../components/Error.svelte";
  import { match } from "../../utils";

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
        goto("auth/profile");
      },
      (err: Error) => {
        throw err;
      }
    );
  }

  const handleAuth = () => (promise = handleLogin());
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
