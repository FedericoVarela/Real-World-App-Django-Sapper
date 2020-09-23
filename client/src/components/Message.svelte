<script lang="ts">
    export let msg : string
    export let level : string
</script>

<style>
    .success {
        color: green;
    }

    .info {
        color: skyblue;
    }

    .warning {
        color: yellow;
    }

    .danger {
        color: red;
    }

</style>

<div class={level} >
    <p>{msg}</p>
</div>