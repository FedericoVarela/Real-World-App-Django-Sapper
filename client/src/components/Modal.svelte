<style>
    div {
        z-index: 100;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        -webkit-box-shadow: 0px 3px 5px -2px rgba(0, 0, 0, 0.88);
        box-shadow: 0px 3px 5px -2px rgba(0, 0, 0, 0.88);
    }
</style>

<div>
    <slot />
</div>
