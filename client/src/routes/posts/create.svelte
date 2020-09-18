<script context="module">
  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "auth/login")
    }
  }
</script>
<script>
  import { stores, goto } from "@sapper/app"
  import { post } from "../../api.ts"
  const { session } = stores()

  const data = {
    title: "",
    content: "",
    draft: false
  };

  async function handleSubmit() {
    const res = await post("blog/posts", data, {
      "Authorization": `Bearer ${$session.user.access_token}`
    })
    // if ($session.postCache === undefined) {
    //   $session.postCache = new Map()
    // }
    // $session.postCache.set(res.id, res)

    goto(`posts/${res.id}`)

    return res
  }
  
</script>

<h1>
  New Article
</h1>

<form on:submit|preventDefault={handleSubmit}>
  <label for="title">Title</label>
  <input class="input" type="text" bind:value={data.title} >

  <label for="content">Content</label>
  <textarea type="text" bind:value={data.content} />
  <input type="checkbox" bind:checked={data.draft} >

  <button type="submit">SUBMIT</button>
</form>

