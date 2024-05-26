<!-- src/routes/data-entry/+page.svelte -->
<script lang="ts">
  import { auth } from '../../firebase-config';
  import { signOut } from 'firebase/auth';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let authenticated = false;

  onMount(() => {
    auth.onAuthStateChanged((user) => {
      if (user) {
        authenticated = true;
      } else {
        goto('/login');
      }
    });
  });

  async function logout() {
    await signOut(auth);
    goto('/login');
  }
</script>

{#if authenticated}
  <main>
    <h1>Data Entry</h1>
    <form>
      <!-- Your data entry form here -->
      <label for="data">Data</label>
      <input id="data" type="text" />

      <button type="submit">Submit</button>
    </form>
    <button on:click={logout}>Logout</button>
  </main>
{:else}
  <p>Loading...</p>
{/if}
