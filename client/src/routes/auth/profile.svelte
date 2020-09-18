<script context="module">
  import { get } from "../../api.ts";

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

<script lang="ts">
  export let data;
  export let ok;

  import { goto, stores } from "@sapper/app";
  import { profileStore } from "../../stores"

  if (ok) {
    console.log(data);
    $profileStore = data
    console.log($profileStore);
  }

  const { session } = stores();
</script>

<h1>{data.username}</h1>
<em>{data.email}</em>
