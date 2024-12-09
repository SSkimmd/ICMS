<script>
    import Sidebar from "../../../components/sidebar/sidebar.svelte";
    let isModalOpen = false;
    let currentFunction;
    export let data;
</script>

<div class="modal" class:modal-open={isModalOpen}>
  <div class="modal-box">
    {#if currentFunction != null}
    <h3 class="font-bold text-2xl pb-4">{currentFunction["function"]}</h3>
    <div>
        {#each Object.keys(currentFunction["arguments"]) as argument}
            <div class="pt-2">
                <p class="pb-2">{argument}</p>
                <input class="input outline outline-2 outline-slate-800" placeholder="Enter Value..."/>
            </div>
        {/each}
    </div>
    <div class="modal-action">
        <button class="btn bg-red-500 hover:bg-red-500 text-red-100" on:click={()=>isModalOpen = false}>Cancel</button>
        <button class="btn bg-green-600 hover:bg-green-700 text-green-100">Send</button>
    </div>
    {/if}
  </div>
</div>

<body>
    <Sidebar/>
</body>

<div class="pl-60 pr-20 pt-20 min-h-screen flex flex-col border-red-400">
    <p class="text-6xl pb-12">Extension: {data["extension"]}</p>
    <div class="grid grid-flow-rows grid-cols-3">
    {#if Object.keys(data).length > 0}
        {#each data["functions"] as func}
        <div class="">
            <div class="flex flex-row items-center">
                <button on:click={() => { isModalOpen = true; currentFunction = func;}} class="btn bg-green-600 hover:bg-green-700  text-green-100 h-12 w-20">Select</button>
                <p class="text-4xl pl-8 pb-8 pt-6">{func["function"]}</p>
            </div>

            <p class="text-2xl pb-2">Arguments</p>          
            {#each Object.keys(func["arguments"]) as argument}
                <p class="text-xl pb-1">{argument}: {func["arguments"][argument]}</p>
            {/each}
        </div>      
        {/each}
    {:else}
        <p class="text-center text-4xl">Server Is Down</p>
        <p class="text-center text-lg">Restart It From The Dashboard To See Active Extensions</p>
    {/if}
    </div>
</div>