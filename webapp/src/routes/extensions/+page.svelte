<script>
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    //import { selected } from "../../lib/sidebar";

    export let data;
</script>


<body>
    <Sidebar/>
</body>

<div class="sm:pl-60 pr-20 pt-20 min-h-screen flex flex-col border-red-400">
    {#if 'server_down' in data}
        <p class="text-center text-4xl">Server Is Down</p>
        <p class="text-center text-lg">Extensions Will Be Displayed Here</p>        
    {:else}
        <p class="text-6xl sm:pl-2 pl-12">Extensions</p>
        <div class="grid grid-flow-row sm:grid-cols-1 2xl:grid-cols-3 xl:grid-cols-2 md:grid-cols-1">
            {#each Object.keys(data) as extension}
                <div class="pt-10">
                    <div class="card bg-base-100 w-96 shadow-2xl">
                        <div class="card-body">
                        <h2 class="card-title">{extension}</h2>
                        <div class="card-actions justify-end">
                            {#if data[extension]["enabled"]}
                                <button class="btn bg-red-500 hover:bg-red-600 text-red-100">Disable</button>
                            {:else}
                                <button class="btn bg-green-600 hover:bg-green-700 text-green-100">Enable</button>
                            {/if}
                            <a href={"/extensions/" + extension} class="btn text-gray-400 border-1">View API</a>
                        </div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>




<style>

</style>