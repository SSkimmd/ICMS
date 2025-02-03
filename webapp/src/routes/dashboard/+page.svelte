<script>
    import { onMount } from "svelte";
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    import Icon from "@iconify/svelte"


    let messages = []
    let showLinesValue = "50";
    async function RefreshServerLog() {
        if(showLinesValue == "") return;

        const response = await fetch("/api/serverlog", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "lines": showLinesValue
            })
        })

        if(response.status == 200) {
            const text = await response.text();
            const lines = text.split('\n');
            messages = lines;
        }
    }

    onMount(async () => {
        await RefreshServerLog();
    })

    export let data;
    export let form;
</script>


<div>
    <Sidebar/>
</div>

<div class="sm:pl-60 pr-20 pt-4 min-h-screen flex flex-col border-red-400 text-2xl">
    <span class="icon-[solar--add-square-linear]" style="width: 24px; height: 24px;"></span>
    <p class="text-6xl">Dashboard</p>
    <div class="flex">
        {#if data["server_running"]}
            <p class="text-6xl text-green-500">.</p>    
            <p class="inline-block pt-8 pl-2 relative">Server's Running</p>
        {:else}
            <p class="text-6xl text-red-500">.</p>  
            <p class="inline-block pt-8 pl-2 relative">Server's Down</p>
        {/if}
    </div>
    <div class="text-lg flex pt-2">
        <form method="POST">
            <button class="btn bg-green-600 hover:bg-green-700 text-green-100" formaction="?/start">
                Start
                <Icon class="w-5 h-5" icon="formkit:start"/>
            </button>
        </form>
        <form method="POST">
            <button class="btn bg-red-500 hover:bg-red-600 text-red-100" formaction="?/stop">
                Stop
                <Icon class="w-5 h-5" icon="ph:stop-duotone"/>
            </button>
        </form>
        <form method="POST">
            <button class="btn bg-amber-400 hover:bg-amber-500 text-amber-800" formaction="?/restart">
                Restart
                <Icon class="w-6 h-6" icon="solar:restart-square-line-duotone"/>
            </button>
        </form>
    </div>
    <div class="pt-8">
        <h1 class="text-4xl">Server Log</h1>
        <div class="divider w-3/5"/>
        <button on:click={ () => { RefreshServerLog(); } } class="btn btn-outline border-gray-600">
            Refresh 
            <Icon class="w-6 h-6" icon="solar:refresh-square-line-duotone"/>
        </button>
        <select bind:value={showLinesValue} class="select select-bordered border-gray-600 w-36 max-w-xs">
            <option disabled>Show Lines</option>
            <option>10</option>
            <option>20</option>
            <option>30</option>
            <option>40</option>
            <option>50</option>
        </select>
        
        <div class="pt-4 overflow-x-auto">
            <div class="scrollbar overflow-x-auto h-52 w-3/5">
                <table class="table table-xs table-pin-rows table-pin-cols">
                <thead>
                <tr>
                    <td>Message</td>
                </tr>
                </thead>
                <tbody>
                    {#each messages as message}
                        <tr>
                            <td>{message}</td>
                        </tr>
                    {/each}
                </tbody>
                </table>
            </div>
        </div>
    </div>
    <div class="pt-8">
        <div class="flex">
            <h1 class="pb-4">Devices</h1>
            <p class="pl-2">0 / 4</p>
        </div>
        <div class="btn-group space-x-4">
            <button class="btn w-72 h-48 hover:border-gray-600 hover:border-2 pb-12">
                <p class="fixed pt-24">Add Device</p>
                <Icon class="w-24 h-12" icon="solar:add-square-line-duotone"></Icon>
            </button>
            <button class="btn w-72 h-48"></button>
            <button class="btn w-72 h-48"></button>
            <button class="btn w-72 h-48"></button>
        </div>
    </div>
</div>