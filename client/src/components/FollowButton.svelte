<script lang="ts">
    export let username;
    let is_following = false;

    async function toggleFollow() {
        //TODO
        is_following = !is_following;
    }
</script>

<button on:click={toggleFollow}>
    +
    {is_following ? 'Unf' : 'F'}ollow
    {username}</button>
