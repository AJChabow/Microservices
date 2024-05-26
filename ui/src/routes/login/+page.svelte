<!-- src/routes/login/+page.svelte -->
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

<main>
  <h1>Login</h1>
  <form on:submit|preventDefault={login}>
    <label for="email">Email</label>
    <input id="email" type="email" bind:value={email} />

    <label for="password">Password</label>
    <input id="password" type="password" bind:value={password} />

    {#if errorMessage}
      <p style="color: red;">{errorMessage}</p>
    {/if}

    <button type="submit">Login</button>
  </form>
</main>
