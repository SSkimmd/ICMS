<script>
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    export let data;
</script>


<body>
    <Sidebar/>
</body>

<div class="pl-60 pr-20 pt-20 min-h-screen flex flex-col border-red-400">
    {#if Object.keys(data).length > 0}
        <p class="text-6xl pb-8">Devices</p>
        <div class="grid grid-flow-row grid-cols-3 gap-2 grid-rows-2">
            {#each Object.keys(data["devices"]) as device}
                <div class="w-auto h-40 border-2 border-blue-500">
                    <p class="w-full h-full pt-12 text-center">
                        {device}
                    </p>
                </div>
            {/each}
        </div>
    {:else}
        <p class="text-center text-4xl">Server Is Down</p>
        <p class="text-center text-lg">Restart It From The Dashboard To See Active Extensions</p>
    {/if}    
</div>

<style>

</style>