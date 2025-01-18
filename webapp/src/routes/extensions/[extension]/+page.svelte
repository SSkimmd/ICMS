<script>
    import Sidebar from "../../../components/sidebar/sidebar.svelte";
    let isModalOpen = false;
    let CurrentFunction;
    let requestResult = "";

    let CurrentFunctionArguments = { }
    let JsonCurrentFunctionArguments = { }

    function SetCurrentFunction(func) {
        CurrentFunction = func;
        CurrentFunctionArguments = { }

        const args = Object.keys(CurrentFunction["arguments"]);
        for(var key in args) {
            CurrentFunctionArguments[args[key]] = "";
        }

        JsonCurrentFunctionArguments = JSON.stringify(CurrentFunctionArguments, null, "\t");
    }

    async function SendAPIRequest() {
        if(CurrentFunction == null) return;
        if(data == null) return;

        CurrentFunctionArguments = JsonCurrentFunctionArguments.replace(/\s+/g, "");
        
        const response = await fetch("/api/extensions", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "type": "POST",
                "module": data["extension"],
                "function": CurrentFunction["function"],
                "arguments": JSON.parse(CurrentFunctionArguments)
            })
        })

        const jsonResponse = await response.json();
        requestResult = jsonResponse;
    }

    export let data;
    export let form;
</script>

<div class="modal" class:modal-open={isModalOpen}>
    <div class="modal-box">
        {#if CurrentFunction != null}
        <h3 class="font-bold text-2xl pb-4">{CurrentFunction["function"]}</h3>
        <div>
            <textarea class="textarea textarea-bordered w-full h-96 text-lg" bind:value={JsonCurrentFunctionArguments}></textarea>
        </div>
        <div class="modal-action">
            <button class="btn bg-red-500 hover:bg-red-500 text-red-100" on:click={() => {
                isModalOpen = false; JsonCurrentFunctionArguments = ""; requestResult = ""
            }}>Cancel</button>
            <button class="btn bg-green-600 hover:bg-green-700 text-green-100" on:click={() => SendAPIRequest()}>Send</button>
        </div>
        {#if requestResult != ""}
            <p>{requestResult["status"]}</p>
            <p>{requestResult["response"]}</p>
        {/if}
        {/if}
    </div>
</div>

<body>
    <Sidebar/>
</body>

<div class="sm:pl-60 pr-20 pt-20 min-h-screen flex flex-col">
    <p class="text-6xl pb-12">Extension: {data["extension"]}</p>
    <div class="grid grid-flow-row sm:grid-cols-1 2xl:grid-cols-3 xl:grid-cols-2 md:grid-cols-1">
    {#if Object.keys(data).length > 0}
        {#each data["functions"] as func}
        <div class="flex flex-col">
            <div class="card bg-base-100 w-96 shadow-2xl">
                <div class="card-body">
                    <h2 class="card-title text-3xl text-zinc-300">{func["function"]}</h2>
                    <p class="text-xl">Arguments</p>
                    {#each Object.keys(func["arguments"]) as argument}
                        <p class="text-sm">{argument}: {func["arguments"][argument]}</p>
                    {/each}
                    <div class="card-actions justify-end">
                        <button on:click={() => { isModalOpen = true; SetCurrentFunction(func);}} class="btn bg-green-600 hover:bg-green-700  text-green-100 h-12 w-20">Select</button>
                    </div>
                </div>
            </div>    
        </div>  
        {/each}
    {:else}
        <p class="text-center text-4xl">Server Is Down</p>
        <p class="text-center text-lg">Restart It From The Dashboard To See Active Extensions</p>
    {/if}
    </div>
</div>