<script>
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    import Icon from "@iconify/svelte"

    export let data;
    export let form;
</script>


<div>
    <Sidebar/>
</div>

<div class="sm:pl-60 pr-20 pt-20 min-h-screen flex flex-col border-red-400 text-2xl">
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

    <div class="text-lg flex pt-2">
        <form method="POST">
            <button class="btn bg-green-600 hover:bg-green-700 text-green-100" formaction="?/start">Start</button>
        </form>

        <form method="POST">
            <button class="btn bg-red-500 hover:bg-red-600 text-red-100" formaction="?/stop">Stop</button>
        </form>

        <form method="POST">
            <button class="btn bg-amber-400 hover:bg-amber-500 text-amber-800" formaction="?/restart">Restart</button>
        </form>
    </div>
</div>



<style>

</style>