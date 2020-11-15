<script lang="ts">
  import { stores, goto } from "@sapper/app";
  import UIError from "../../components/Error.svelte";
  import { post, User } from "../../api";
  import { match } from "../../utils";
  import type { Result } from "../../types";

  const { session } = stores();

  const data = {
    username: "",
    email: "",
    password: "",
  };

  let confirmPw = "";
  let error: Error;

  $: pwMatch = data.password === confirmPw;

  async function handleSubmit() {
    const res = await post("register", data);
    match(
      res,
      async (_) => {
        const redirect: Result<User> = await User.login(
          data.username,
          data.password
        );
        match(
          redirect,
          (user: User) => {
            $session.user = user;
            goto("auth/profile");
          },
          (err: Error) => (error = err)
        );
      },
      (err: Error) => (error = err)
    );
  }
</script>

{#if error}
  <UIError data={error} />
{/if}

<form on:submit|preventDefault={handleSubmit}>
  {#if !pwMatch}
    <UIError data={new Error('{"detail": "Passwords don\'t match"}')} />
  {/if}

  <label for="username">Username</label>
  <input type="text" bind:value={data.username} />

  <label for="email">Email</label>
  <input type="text" bind:value={data.email} />

  <label for="password">Password</label>
  <input type="password" bind:value={data.password} />

  <label for="password">Confirm Password</label>
  <input type="password" bind:value={confirmPw} />

  <button type="submit">SUBMIT</button>
</form>
