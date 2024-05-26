<!-- src/routes/register/+page.svelte -->
<script lang="ts">
  import { auth } from '../../firebase-config';
  import { createUserWithEmailAndPassword } from 'firebase/auth';
  import { goto } from '$app/navigation';

  let email = '';
  let password = '';
  let errorMessage = '';

  async function register() {
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      goto('/login');
    } catch (error) {
      errorMessage = error.message;
    }
  }
</script>

<main>
  <h1>Register</h1>
  <form on:submit|preventDefault={register}>
    <label for="email">Email</label>
    <input id="email" type="email" bind:value={email} />

    <label for="password">Password</label>
    <input id="password" type="password" bind:value={password} />

    {#if errorMessage}
      <p style="color: red;">{errorMessage}</p>
    {/if}

    <button type="submit">Register</button>
  </form>
</main>
