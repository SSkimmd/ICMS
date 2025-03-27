<script>
    import { goto } from '$app/navigation'
    export let data;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="h-screen flex items-center justify-center font-[roboto]"> 
    <div class="pr-20 h-2/3">
        <ul>
            <li class="text-2xl text-slate-300 font-medium">
                <a href="/devices">Devices</a>
            </li>
            <li class="text-lg">
                <button>Pico</button>
            </li>
            <li class="text-lg">
                <button>Pico-W</button>
            </li>
        </ul>
        <div class="divider"></div>
        <ul>
            <li class="text-2xl text-slate-300 font-medium">
                <a href="/extensions">Extensions</a>
            </li>
            <li class="text-lg">Popular</li>
            <li class="text-lg">Highest Rated</li>
        </ul>
    </div>
    <div class="w-2/3 h-2/3 text-white rounded-lg">
        <button on:click={() => { goto("/creator") }} class="btn btn-soft float-end">
            Create +
        </button>
        <div class="text-4xl font-medium">Devices</div>
        <div class="pt-4 grid grid-flow-row grid-cols-4 grid-rows-2 gap-6 w-fit h-fit">
            {#each Object.keys(data) as device}
            <div class="card bg-base-200 h-80 w-72 shadow-sm hover:bg-base-300" on:click={() => { goto("/devices/" + device) }}>
                <figure>
                    <img
                    src="https://img.daisyui.com/images/stock/photo-1606107557195-0e29a4b5b4aa.webp"
                    alt="Shoes" />
                </figure>
                <div class="card-body">
                    <h2 class="card-title select-none">{data[device]["name"]}</h2>
                    <div class="h-14 w-full">
                        <p class="overflow-hidden text-ellipsis">{data[device]["description"]}</p>
                    </div>
                </div>
            </div>     
            {/each}
        </div>
    </div>
</div>

<svelte:head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
    </style>
</svelte:head>