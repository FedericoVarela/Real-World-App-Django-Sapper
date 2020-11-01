<script context="module" lang="ts">
  import { get } from "../../api";
  import { match } from "../../utils"

  interface Profile {
    username: string,
    created_at: Date,
    description: string,
    picture: URL
  }

  export async function preload(page, session) {
    if (session.user === undefined) {
      return this.redirect(302, "auth/login");
    } else {
      const res = await get<Profile>(`profile/${session.user.username}`, {
        Authorization: `Bearer ${session.user.access_token}`,
      });

      return match(
      res,
      (prof: Profile) => prof,
      (err) => {throw err}
      )
    }
  }
</script>

<script lang="ts">  
  export let username;
  export let created_at;
  export let description;
  export let picture;
</script>

<h1>{username}</h1>
<img src={picture} alt={`${username}'s profile picture`}>
<em>{created_at}</em>
<p>{description ? description : "This user has no description"}</p>
<a href="auth/change-password">Change Password</a>