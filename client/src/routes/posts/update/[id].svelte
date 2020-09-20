<script context="module">
  import { get } from "../../../api";
  export async function preload({ params }, session) {
    if (session.user === undefined) {
      console.log(session.user);
      return this.redirect(302, "auth/login");
    } else {
      const { id } = params;
      const data = await get(this.fetch, `blog/posts/${id}`);
      return { data: data.data };
    }
  }
</script>

<script>
  import { stores, goto } from "@sapper/app"
  import { isOK } from "../../../api.ts"

  export let data;
  const { session } = stores()
  const { id, title, content } = data;

  let formData = {
    title: title,
    content: content,
  };

  async function handleSubmit() {
      const res = await $session.user.patch(`blog/posts/${id}`, formData)
      if (isOK(res)) {
        goto(`posts/${id}`)
      } else {
        goto("posts")
      }
  }

</script>

<form on:submit|preventDefault={handleSubmit}>
  <h1><input type="text" bind:value={formData.title} /></h1>
  <input type="text" bind:value={formData.content} />
  <button type="submit">UPDATE</button>
</form>
