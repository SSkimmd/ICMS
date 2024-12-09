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
                <a href={"/devices/" + device} class="w-auto h-40 bg-gray-800 rounded-xl shadow-xl">
                    <p class="w-full h-full pt-14 text-2xl text-center">
                        {device}
                    </p>
                </a>
            {/each}
        </div>
    {:else}
        <p class="text-center text-4xl">No Devices Connected</p>
        <p class="text-center text-lg">Connected Devices Will Be Displayed Here</p>
    {/if}    
</div>

<style>

</style>