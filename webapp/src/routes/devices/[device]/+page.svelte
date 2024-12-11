<script>
    import Sidebar from "../../../components/sidebar/sidebar.svelte";
    export let data;
</script>


<body>
    <Sidebar/>
</body>

<div class="sm:pl-60 pr-20 pt-20 min-h-screen flex flex-col">
    <p class="text-6xl pb-12">Device: {data["device"]}</p>
    <div class="grid grid-flow-rows grid-cols-3">
    </div>
</div>