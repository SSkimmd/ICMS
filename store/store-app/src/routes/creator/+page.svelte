<script>
</script>

<!-- svelte-ignore a11y-missing-attribute -->
<!-- svelte-ignore a11y-missing-attribute -->
<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
<body class="w-screen font-[roboto]">
    <dialog id="NewDeviceModal" class="modal h-full">
        <div class="modal-box">
            <form method="dialog">
                <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
            </form>
            <h3 class="text-lg font-bold">New Device</h3>
            <form method="POST" action="?/upload" enctype="multipart/form-data">
                <fieldset class="fieldset">
                    <legend class="fieldset-legend">Select Packaged Device File</legend>
                    <input 
                    name="fileInput" type="file" accept=".zip, .rar, .7zip" multiple="false" class="file-input file-input-ghost"/>
                </fieldset>
                <div class="modal-action">
                    <button class="btn btn-soft">Upload</button>
                </div>
            </form>
        </div>
    </dialog>


    <div class="pt-24 flex items-center justify-center"> 
        <div class="h-2/3">
            <div class="">
            </div>
        </div>
    </div>
    <div class="flex items-center justify-center pt-4">
        <div class="h-96 w-1/2 rounded-lg">
            <p class="pt-12 text-3xl pb-4">Uploads</p>
            <div class="flex space-x-2">
                <form class="filter">
                    <input class="btn btn-square" type="reset" value="x"/>
                    <input class="btn" type="radio" name="uploads" aria-label="Devices"/>
                    <input class="btn" type="radio" name="uploads" aria-label="Extensions"/>
                </form>
                <div>
                    <label class="input">
                        <svg class="h-4 opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></g></svg>
                        <input type="search" class="grow" placeholder="Search" />
                      </label>
                </div>
                <div class="ml-auto">
                    <button onclick="NewDeviceModal.showModal()" class="btn btn-soft">
                        New Upload
                    </button>
                </div>
            </div>
            <div class="pt-4"></div>
            <div class="overflow-x-auto rounded-box border border-base-content/10 bg-base-100">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Type</th>
                      <th>Downloads</th>
                      <th>Details</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                        <td>Spotify</td>
                        <td>Extension</td>
                        <td>90,000</td>
                        <td class="btn btn-link">View</td>
                        <td class="btn btn-link">Edit</td>
                    </tr>
                  </tbody>
                </table>
              </div>
        </div>
    </div>
</body>

<svelte:head>
    <style>
        
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
    </style>
</svelte:head>