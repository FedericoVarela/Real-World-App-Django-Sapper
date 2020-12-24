<style>
    div {
        z-index: 100;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        -webkit-box-shadow: 0px 3px 5px -2px rgba(0, 0, 0, 0.88);
        box-shadow: 0px 3px 5px -2px rgba(0, 0, 0, 0.88);
        padding: 50px;
        -webkit-box-shadow: -1px 0px 30px 300px rgba(0, 0, 0, 0.27);
        -moz-box-shadow: -1px 0px 30px 300px rgba(0, 0, 0, 0.27);
        box-shadow: -1px 0px 30px 100vh rgba(0, 0, 0, 0.27);
    }
</style>

<div>
    <slot />
</div>
