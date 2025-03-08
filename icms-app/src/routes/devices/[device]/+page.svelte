<script>
    import Sidebar from "../../../components/sidebar/sidebar.svelte";
    export let data;

    let isModalOpen = false;

    let CurrentFunctionArguments = "";
    let JsonCurrentFunctionArguments = "";
    let requestResult = "";

    async function SendAPIRequest() {
        CurrentFunctionArguments = JsonCurrentFunctionArguments.replace(/\s+/g, "");
        
        const response = await fetch("/api/device", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "device": data["device_name"],
                "function": "test",
                "arguments": JSON.parse(CurrentFunctionArguments)
            })
        })

        const jsonResponse = await response.json();

        requestResult = jsonResponse;
    }
</script>


<div class="modal" class:modal-open={isModalOpen}>
    <div class="modal-box">
        <h3 class="font-bold text-2xl pb-4">Send Device Message</h3>
        <div>
            <textarea bind:value={JsonCurrentFunctionArguments} class="textarea textarea-bordered w-full h-96 text-lg font-mono"></textarea>
        </div>
        <div class="modal-action">
            <button class="btn bg-red-500 hover:bg-red-500 text-red-100" on:click={() => {
                isModalOpen = false;
            }}>Cancel</button>
            <button on:click={() => { SendAPIRequest(); }} class="btn bg-green-600 hover:bg-green-700 text-green-100">Send</button>
        </div>
    </div>
</div>

<body>
    <Sidebar/>
</body>

<div class="sm:pl-60 pr-20 pt-20 min-h-screen flex flex-col">
    <p class="text-6xl pb-12">Device: {data["name"]}</p>
    <div class="grid grid-flow-rows grid-cols-3">
        <button on:click={() => { isModalOpen = true; }} class="btn bg-green-600 hover:bg-green-700  text-green-100 h-12 w-48">Send Message</button>
    </div>
</div>