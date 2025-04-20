<script>
	let showToast = false;
    export let form;
</script>

<div class="hero min-h-screen flex bg-base-200 justify-center">
	<div class="hero-content">
	  <div class="text-center lg:text-left">
		<p class="py-6"></p>
	  </div>
	  	<div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
		<form method="POST" class="card-body">
		  <div class="form-control">
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label class="label">
			  <span class="label-text">Username</span>
			</label>
			<input name="username" type="username" placeholder="username" class="input input-bordered" required/>
		  </div>
		  <div class="form-control">
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label class="label">
			  <span class="label-text">Password</span>
			</label>
			<input name="password" type="password" placeholder="password" class="input input-bordered" required/>
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label class="label">
			  <!-- svelte-ignore a11y-invalid-attribute -->
			  <a href="#" class="label-text-alt link link-hover">Forgot password?</a>
			</label>
		  </div>
		  <div class="form-control mt-6">
			<button class="btn btn-primary" formaction="?/login">Login</button>
		  </div>
		</form>
		</div>
	</div>
	<div class="hero-content flex-col lg:flex-row-reverse">
		<div class="text-center lg:text-left">
		  <p class="py-6"></p>
		</div>
			<div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
		  <form method="POST" class="card-body">
			<div class="form-control">
			  <!-- svelte-ignore a11y-label-has-associated-control -->
			  <label class="label">
				<span class="label-text">Username</span>
			  </label>
			  <input name="username" type="username" placeholder="username" class="input input-bordered" required/>
			</div>
			<div class="form-control">
			  <!-- svelte-ignore a11y-label-has-associated-control -->
			  <label class="label">
				<span class="label-text">Password</span>
			  </label>
			  <input name="password" type="password" placeholder="password" class="input input-bordered" required/>
			  <!-- svelte-ignore a11y-label-has-associated-control -->
			  <label class="label">
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a href="#" class="label-text-alt link link-hover">Forgot password?</a>
			  </label>
			</div>
			<div class="form-control mt-6">
			  <button class="btn btn-primary" formaction="?/register">Register</button>
			</div>
		  </form>
		  </div>
	  </div>
</div>