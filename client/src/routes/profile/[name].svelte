<script context="module" lang="ts">
	import { maybe_authorized_get } from "../../api";
	import { match } from "../../utils";
	import type { Profile } from "../../types";
	import UserProfile from "../../components/UserProfile.svelte";

	export async function preload({ params }, session) {
		const { name } = params;
		const res = await maybe_authorized_get<Profile>(`profile/${name}`, session.user);
		return match(
			res,
			(data: Profile) => {
				return { data };
			},
			(_: Error) => {
				this.error(404, "Not found");
			}
		);
	}
</script>

<script lang="ts">
	export let data: Profile;
</script>

<UserProfile {data} />
