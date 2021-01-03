<script context="module">
    export async function preload(page, session) {
        if (session.user === undefined) {
            return this.redirect(302, "user/login");
        }
    }
</script>

<script lang="ts">
    import { stores, goto } from "@sapper/app";
    import { match } from "../../utils";
    import UIError from "../../components/Error.svelte";

    const { session } = stores();

    let oldPassword: string;
    let newPassword: string;
    let error: Error;

    async function submit() {
        const res = await $session.user.post("change-password", {
            old_password: oldPassword,
            new_password: newPassword,
        });
        return match(
            res,
            (_) => goto("user/profile"),
            (err: Error) => {
                error = err;
            }
        );
    }
</script>

{#if error}
    <UIError data={error} />
{/if}

<h1>Change password</h1>

<form on:submit|preventDefault={submit}>
    <label for="old">Old Password</label>
    <input type="password" bind:value={oldPassword} id="old" required />
    <label for="new">New Password</label>
    <input type="password" bind:value={newPassword} id="new" required />

    <button type="submit">CHANGE PASSWORD</button>
</form>
