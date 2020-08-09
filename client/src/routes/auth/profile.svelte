<script context="module">
  import { get } from "../../api";
  import axios from "axios"

  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "auth/login");
    } else {
      const res = await get(this.fetch, "users/me", {
          "Authorization": `Bearer ${session.user.access_token}`
      })
      return {res}


    }
  }
</script>

<script>
  export let res;
  import { goto, stores } from "@sapper/app";

  let token;
  const { session } = stores();
</script>

<h1>{res.username}</h1>
<em>{res.email}</em>

