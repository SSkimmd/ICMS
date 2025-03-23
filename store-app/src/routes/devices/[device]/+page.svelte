<script>
    import { goto } from '$app/navigation'
    export let data;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="h-screen flex items-center justify-center font-[roboto]">
    <div class="w-2/3 h-3/4 text-white rounded-lg">
        <div class="text-4xl">
            {data["name"]}
            <button class="btn btn-soft btn-success">
                Get Device
            </button>
            <div>
                <figure class="w-96 h-96 pt-20">
                    <img
                    src="https://img.daisyui.com/images/stock/photo-1606107557195-0e29a4b5b4aa.webp"
                    alt="Shoes" />
                </figure>
            </div>
        </div>
        <div class="text-3xl pt-4">
            Overview
            <div class="text-xl">{data["description"]}</div>
        </div>
        <div class="pt-12 grid grid-cols-4">
            <div class="text-2xl">
                Downloads
                <div class="text-lg">90,000</div>
            </div>
            <div class="text-2xl">
                Version
                <div class="text-lg">1.1.0</div>
            </div>
            <div class="text-2xl">
                Author
                <div class="text-lg">{data["author"]}</div>
            </div>
            <div class="text-2xl">
                Compatibility
                <div class="text-lg">
                    {#each data["compatibility"] as device}
                        <p>{device}</p>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</div>

<svelte:head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
    </style>
</svelte:head>






