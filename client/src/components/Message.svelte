<script>
    export let msg
    export let level
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