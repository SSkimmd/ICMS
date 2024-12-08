<script>
    import Sidebar from "../../../components/sidebar/sidebar.svelte";
    export let data;
</script>



<body>
    <Sidebar/>
</body>

<div class="pl-60 pr-20 pt-20 min-h-screen flex flex-col border-red-400">
    {#if Object.keys(data).length > 0}
        {#each data["functions"] as func}
            <p class="text-6xl pb-8">{func["function"]}</p>
            <p class="text-2xl pb-2">Arguments</p>
            
            {#each Object.keys(func["arguments"]) as argument}
                <p class="text-xl pb-1">{argument}: {func["arguments"][argument]}</p>
            {/each}      
        {/each}
    {:else}
        <p class="text-center text-4xl">Server Is Down</p>
        <p class="text-center text-lg">Restart It From The Dashboard To See Active Extensions</p>
    {/if}
</div>