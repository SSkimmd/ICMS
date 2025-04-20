<script>
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    import Icon from "@iconify/svelte";
    export let data;

    let newDeviceModalOpen = false;
    let nameDeviceModalOpen = false;

    let connections = data["connections"];
    let devices = data["devices"];
    let selectedConnection = "";


    let deviceName = "";
    let deviceType = "";
    let addDeviceResponse = null;

    function CancelDeviceCreation() {
        deviceName = "";
        deviceType = "";
        addDeviceResponse = null;
        newDeviceModalOpen = false;
        nameDeviceModalOpen = false;
    }

    async function CreateDevice() {
        if(deviceName == "") return;
        if(deviceType == "" && deviceType != "Device Type") return;

        const response = await fetch("/api/devices", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "connection_name": selectedConnection,
                "device_name": deviceName,
                "device_type": deviceType
            })
        })

        const jsonResponse = await response.json();
        return jsonResponse;
    }
</script>


<body>
    <Sidebar/>
</body>

<div class="modal" class:modal-open={nameDeviceModalOpen}>
    <div class="modal-box">
        <h3 class="font-bold text-2xl pb-2">Setup New Device</h3>
        <div>
            <input bind:value={deviceName} class="input input-bordered w-full max-w-s" placeholder={selectedConnection}>
            <div class="pt-2">
                <select bind:value={deviceType} class="select select-bordered w-full max-w-xs">
                    <option disabled selected>Device Type</option>
                    <option>Input</option>
                    <option>Output</option>
                    <option>Both</option>
                </select>
            </div>
        </div>
        <div class="modal-action">
            <button on:click={() => { CancelDeviceCreation(); }} class="btn bg-red-500 hover:bg-red-500 text-red-100">Cancel</button>
            <button on:click={() => { nameDeviceModalOpen = false; newDeviceModalOpen = true; }} class="btn bg-slate-400 hover:bg-slate-500 text-slate-700">Back</button>
            <button on:click={async () => { 
                const response = await CreateDevice();
                addDeviceResponse = response;
                CancelDeviceCreation();
            }} class="btn bg-green-600 hover:bg-green-700 text-green-100">Finish</button>
        </div>
    </div>
</div>

<div class="modal" class:modal-open={newDeviceModalOpen}>
    <div class="modal-box">
        <h3 class="font-bold text-2xl pb-2">Add New Device</h3>
        <p class="pb-2">Available Connections</p>
        <ul class="bg-gray-800 rounded-md">
            {#if connections}
                {#each connections as connection}
                <li>
                    <input type="radio" id="connection" on:click={() => { selectedConnection = connection; }} class="hidden peer btn">
                    <label for="connection" class="btn w-full peer-checked:border-2 peer-checked:border-slate-500">{connection}</label>
                </li>
                {/each}
            {/if}
        </ul>
        <div class="modal-action">
            <button on:click={() => { CancelDeviceCreation(); }} class="btn bg-red-500 hover:bg-red-500 text-red-100">Cancel</button>
            <button on:click={() => {
                if(selectedConnection != "") {
                    newDeviceModalOpen = false; 
                    nameDeviceModalOpen = true; 
                }
            }} class="btn bg-green-600 hover:bg-green-700 text-green-100">Next</button>
        </div>
    </div>
</div>

<div class="sm:pl-60 pr-20 pt-20 min-h-screen flex flex-col">
    {#if 'server_down' in data}
        <p class="text-center text-4xl">Server Is Down</p>
        <p class="text-center text-lg">Connected Devices Will Be Displayed Here</p>        
    {:else}
        <div>
            <p class="text-6xl sm:pl-2 pl-12 pb-10">Devices</p>
            <button on:click={() => { newDeviceModalOpen = true; }} class="btn bg-green-600 hover:bg-green-700 text-green-100">
                <Icon class="w-5 h-5" icon="gala:add"/>
                Add Device
            </button>
            <button on:click={() => { }} class="btn bg-red-500 hover:bg-red-500 text-red-100">
                <Icon class="w-5 h-5" icon="gala:remove"/>
                Remove Device
            </button>
        </div>
        <div class="grid grid-flow-row sm:grid-cols-1 2xl:grid-cols-3 xl:grid-cols-2 md:grid-cols-1">
            <div class="pt-10">
                {#if devices}
                    {#each Object.keys(devices) as device}
                        <div class="card bg-base-100 w-96 shadow-2xl">
                            <div class="card-body">
                            <h2 class="card-title">{devices[device]["device_name"]}</h2>
                            <div class="card-actions justify-end">
                                <a href={"/devices/" + device} class="btn bg-slate-400 hover:bg-slate-500 text-slate-700">View Details</a>
                            </div>
                            </div>
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    {/if}
</div>

<style>

</style>