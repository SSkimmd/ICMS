<script>
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    export let data;
</script>


<body>
    <Sidebar/>
</body>

<div class="pl-60 pr-20 pt-20 min-h-screen flex flex-col border-red-400">
    {#if Object.keys(data).length > 0}
        <p class="text-6xl pb-8">Extensions</p>
        <div class="grid grid-flow-row grid-cols-3 gap-2 grid-rows-2">
            {#each Object.keys(data) as module}
                <a href={"/extensions/" + module} class="w-auto h-40 bg-gray-800 rounded-xl shadow-xl">
                    <p class="w-full h-full pt-14 text-2xl text-center">
                        {module}
                    </p>
                </a>
            {/each}
        </div>
    {:else}
        <p class="text-center text-4xl">Server Is Down</p>
        <p class="text-center text-lg">Restart It From The Dashboard To See Active Extensions</p>
    {/if}
</div>




<style>

</style>