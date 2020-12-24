<script context="module" lang="ts">
  import { match } from "../../utils";
  import type { Profile } from "../../types";

  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "user/login");
    } else {
      const res = await session.user.get(`profile/${session.user.username}`);
      return match(
        res,
        (data: Profile) => {
          return { data };
        },
        (err: Error) => {
          throw err;
        }
      );
    }
  }
</script>

<script lang="ts">
  import UserProfile from "../../components/UserProfile.svelte";

  export let data: Profile;
</script>

<UserProfile {data} />
