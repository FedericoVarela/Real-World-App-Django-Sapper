<script context="module">
  import { get } from "../../api";
  import axios from "axios";

  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "auth/login");
    } else {
      const { data, ok } = await get(this.fetch, "users/me", {
        Authorization: `Bearer ${session.user.access_token}`,
      });

      return { data, ok };
    }
  }
</script>

<script>
  export let data;
  export let ok;

  import { goto, stores } from "@sapper/app";

  const { session } = stores();

  //Mutate the store here because it can't be done in preload
  if (ok) {
    $session.user.username = data.username
  }
</script>

<h1>{data.username}</h1>
<em>{data.email}</em>
