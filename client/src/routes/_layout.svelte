<script>
	import { onMount } from "svelte"
	import { stores } from "@sapper/app"

	import { User } from "../api"
	import Nav from '../components/Nav.svelte';

	export let segment;
	const { session } = stores()

	onMount(async function() {
		$session.user = await User.fromSession()
	})

</script>

<style>
	main {
		position: relative;
		max-width: 56em;
		background-color: white;
		padding: 2em;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>

<Nav {segment}/>

<main>
	<slot></slot>
</main>