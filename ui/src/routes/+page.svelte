<!-- src/routes/+page.svelte -->
<script lang="ts">
    import {Button} from 'flowbite-svelte';
    import {goto} from '$app/navigation';
</script>

<h1 class="text-3xl font-bold mb-4">Welcome to Cropminds Irrigation Calculator App</h1>
<p class="mb-4">Manage your fields, recieve weekly whatsapp messages, and update your data all in one place..</p>
<div class="space-x-4">
    <Button on:click={() => goto('/fields')}>Manage Fields</Button>
    <Button on:click={() => goto('/whatsapp')}>Send WhatsApp Message</Button>
    <Button on:click={() => goto('/data-entry')}>Modify data</Button>
</div>