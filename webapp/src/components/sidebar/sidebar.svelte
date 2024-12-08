<script>
    import { get } from "svelte/store";
    import { selected } from "../../lib/sidebar"

    $: IsSelected = (index) => {
        if(get(selected) == index) {
            return "bg-gray-700"
        } else {
            return ""
        }
    }
</script>

<div class="flex flex-col items-center w-40 h-screen overflow-hidden fixed text-gray-400 bg-gray-900 rounded">
    <a class="flex items-center w-full px-3 mt-3" href="">
        <span class="ml-2 text-sm font-bold">The App</span>
    </a>
    <div class="w-full px-2">
        <div class="flex flex-col items-center w-full mt-3 border-t border-gray-700">
            <a on:click={() => {selected.set(1)}} class="flex items-center w-full h-12 px-3 mt-2 rounded {IsSelected(1)} hover:bg-gray-700 hover:text-gray-300" href="/dashboard">
                <span class="ml-2 text-sm font-medium">Dashboard</span>
            </a>
            <a on:click={() => {selected.set(2)}} class="flex items-center w-full h-12 px-3 mt-2 rounded {IsSelected(2)} hover:bg-gray-700 hover:text-gray-300" href="/extensions">
                <span class="ml-2 text-sm font-medium">Extensions</span>
            </a>
            <a on:click={() => {selected.set(3)}} class="flex items-center w-full h-12 px-3 mt-2 rounded {IsSelected(3)} hover:bg-gray-700 hover:text-gray-300" href="/devices">
                <span class="ml-2 text-sm font-medium">Devices</span>
            </a>
        </div>
    </div>
    <a class="flex items-center justify-center w-full h-16 mt-auto bg-gray-800 hover:bg-gray-700 hover:text-gray-300" href="account">
        <span class="ml-2 text-sm font-medium">Account</span>
    </a>
</div>