<script lang="ts">
  import { auth } from '../../firebase-config';
  import { signInWithEmailAndPassword } from 'firebase/auth';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let email = '';
  let password = '';
  let errorMessage = '';

  async function login() {
    try {
      await signInWithEmailAndPassword(auth, email, password);
      goto('/data-entry');
    } catch (error) {
      errorMessage = error.message;
    }
  }

  onMount(() => {
    // Redirect if already authenticated
    auth.onAuthStateChanged((user) => {
      if (user) {
        goto('/data-entry');
      }
    });
  });
</script>

<main class="flex items-center justify-center min-h-screen bg-gray-100">
  <div class="w-full max-w-md p-8 space-y-8 bg-white rounded shadow-md">
    <h1 class="text-2xl font-bold text-center">Login</h1>
    <form on:submit|preventDefault={login} class="space-y-6">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
        <input id="email" type="email" bind:value={email} class="block w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
        <input id="password" type="password" bind:value={password} class="block w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>

      {#if errorMessage}
        <p class="text-sm text-red-500">{errorMessage}</p>
      {/if}

      <div>
        <button type="submit" class="w-full px-4 py-2 text-white bg-indigo-600 rounded-md shadow-sm hover:bg-indigo-700 focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Sign in
        </button>
      </div>
    </form>
    <p class="text-sm text-center text-gray-600">Don't have an account? <a href="/register" class="text-indigo-600 hover:text-indigo-500">Register here</a></p>
  </div>
</main>
