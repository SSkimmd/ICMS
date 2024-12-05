<script>
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    import Icon from "@iconify/svelte"

    export let data;
    export let form;
</script>


<div>
    <Sidebar/>
</div>

<div class="pl-60 pr-20 pt-20 min-h-screen flex flex-col border-red-400 text-2xl">
    <p class="text-6xl pb-8">Dashboard</p>
    
    <div class="flex">
        {#if data["server_running"]}
            <p class="text-6xl text-green-500">.</p>    
            <p class="inline-block pt-8 pl-2 relative">Server Up</p>
        {:else}
            <p class="text-6xl text-red-500">.</p>  
            <p class="inline-block pt-8 pl-2 relative">Server Down</p>
        {/if}
    </div>

    <div class="text-lg flex">
        <form method="POST">
            <button class="pr-2" formaction="?/start">Start</button>
        </form>

        <form method="POST">
            <button formaction="?/stop">Stop</button>
        </form>

        <form method="POST">
            <button class="pl-2" formaction="?/restart">Restart</button>
        </form>
    </div>
</div>



<style>

</style>