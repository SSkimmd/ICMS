<script>
    import { get } from "svelte/store";
    import { selected } from "../../lib/sidebar"
    import Icon from "@iconify/svelte";

    $: IsSelected = (index) => {
        if(get(selected) == index) {
            return "bg-gray-700"
        } else {
            return ""
        }
    }
</script>

<div class="flex-col items-center w-40 h-screen overflow-hidden fixed hidden sm:flex sm:visible invisible text-gray-400 bg-gray-900 rounded">
    <a class="flex items-center w-full px-3 mt-3" href="/">
        <span class="ml-2 text-sm font-bold">ICMS</span>
    </a>
    <div class="w-full px-2">
        <div class="flex flex-col items-center w-full mt-3 border-t border-gray-700">
            <a on:click={() => {selected.set(1)}} class="flex items-center w-full h-12 px-3 mt-2 rounded {IsSelected(1)} hover:bg-gray-700 hover:text-gray-300" href="/dashboard">
                <Icon class="w-5 h-5" icon="hugeicons:dashboard-square-01"/>
                <span class="flex ml-2 text-sm font-medium">
                    Dashboard
                </span>
            </a>
            <a on:click={() => {selected.set(2)}} class="flex items-center w-full h-12 px-3 mt-2 rounded {IsSelected(2)} hover:bg-gray-700 hover:text-gray-300" href="/extensions">
                <Icon class="w-6 h-6" icon="famicons:extension-puzzle-outline"/>
                <span class="flex ml-2 text-sm font-medium">
                    Extensions
                </span>
            </a>
            <a on:click={() => {selected.set(3)}} class="flex items-center w-full h-12 px-3 mt-2 rounded {IsSelected(3)} hover:bg-gray-700 hover:text-gray-300" href="/devices">
                <Icon class="w-6 h-6" icon="ph:devices-light"/>
                <span class="flex ml-2 text-sm font-medium">
                    Devices
                </span>
            </a>
        </div>
    </div>
    <a on:click={() => {selected.set(4)}} class="flex items-center justify-center w-full h-16 mt-auto bg-gray-800 {IsSelected(4)} hover:bg-gray-700 hover:text-gray-300" href="account">
        <Icon class="w-7 h-7" icon="ic:sharp-manage-accounts"/>
        <span class="flex ml-2 text-sm font-medium">
            Profile
        </span>
    </a>
</div>