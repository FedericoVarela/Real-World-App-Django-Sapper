<style>
    div {
        z-index: 100;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 50px;
    }
</style>

<div class="modal" >
    <slot />
</div>
