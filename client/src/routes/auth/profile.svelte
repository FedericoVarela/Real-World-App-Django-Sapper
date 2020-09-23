<script context="module" lang="ts">
  import { get } from "../../api";
  import { match } from "../../utils"
  import type { AxiosResponse } from "axios"

  interface Profile {
    username: string,
    email: string
  }

  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "auth/login");
    } else {
      const res = await get<Profile>("users/me", {
        Authorization: `Bearer ${session.user.access_token}`,
      });

      return match(
      res,
      (prof: AxiosResponse<Profile>) => prof.data,
      (err) => {throw err}
      )
    }
  }
</script>

<script lang="ts">  
  export let username;
  export let email;
</script>

<h1>{username}</h1>
<em>{email}</em>
