<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import "../app.css";
  import { goto } from '$app/navigation';
  import { auth } from '../firebase-config';

  onMount(async () => {
    auth.onAuthStateChanged((user) => {
      if (!user) {
        goto('/login');
      }
    });
  });
</script>

<slot />
