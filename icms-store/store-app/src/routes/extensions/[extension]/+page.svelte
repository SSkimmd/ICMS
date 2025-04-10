<script>
    import { goto } from '$app/navigation'

    async function GetDownload() {
        const extension = data["extension_name"];
        const response = await fetch("/api/store/extensions/download", {
            method: "POST",
            body: JSON.stringify({
                'extension': extension
            })
        })

        const blob = await response.blob();
        console.log(blob);

        var url = window.URL || window.webkitURL;
        let link = url.createObjectURL(blob);
        let a = document.createElement("a");
        a.setAttribute("download", extension + ".zip");
        a.setAttribute("href", link);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }


    export let data;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="h-screen flex items-center justify-center font-[roboto]">
    <div class="w-2/3 h-3/4 text-white rounded-lg">
        <div class="text-4xl">
            <div class="flex space-x-4">
                <p>{data["name"]}</p>
                <button on:click={async() => { GetDownload(); }} class="btn btn-soft btn-success">
                    Get Extension
                </button>
            </div>
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
        <div class="pt-12 grid grid-cols-3">
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
        </div>
    </div>
</div>

<svelte:head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
    </style>
</svelte:head>






