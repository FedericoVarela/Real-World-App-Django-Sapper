<script>
  import { stores, goto } from "@sapper/app";
  import Message from "../../components/Message.svelte";
  import { post, User } from "../../api.ts";

  const { session } = stores();

  const data = {
    username: "",
    email: "",
    password: "",
  };

  let confirmPw = "";
  let error = false;

  $: pwMatch = data.password === confirmPw;

  async function handleSubmit() {
    const res = await post("users", data);
    console.log(res);
    if (res instanceof Error) {
      error = res.message;
    } else {
      $session.user = await User.login(data.username, data.password);
      goto(`auth/profile`);
    }
  }
</script>

{#if error}{error}{/if}

<form on:submit|preventDefault={handleSubmit}>
  {#if !pwMatch}
    <Message msg="Passwords don't match" level="danger" />
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
