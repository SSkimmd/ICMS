<script>
    import Sidebar from "../../components/sidebar/sidebar.svelte";
    import Icon from "@iconify/svelte";
    import Page from "../devices/+page.svelte";
</script>


<div>
    <Sidebar/>
</div>

<div class="sm:pl-60 pr-20 pt-16 min-h-screen flex flex-col border-red-400 text-2xl">
    <p class="text-6xl">Account options</p>
    <div class="divider w-3/5 pt-2"/>
    <div class="pb-4 text-3xl">Personal Information</div>
    <div class="btn-group space-x-1">
        <button class="btn btn-outline border-gray-500 w-48">
            <Icon class="w-6 h-6" icon="solar:password-outline"></Icon>
            Reset Password
        </button>
        <button class="btn btn-outline border-gray-500 w-52">
            <Icon class="w-6 h-6" icon="solar:user-id-linear"></Icon>
            Update Username
        </button>
    </div>
    <div class="pt-16 text-3xl">Account Information</div>
    <p class="pt-2 text-xl">Roles</p>
</div>




<style>

</style>