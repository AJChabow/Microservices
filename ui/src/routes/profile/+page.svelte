<!-- src/routes/profile/+page.svelte -->
<script lang="ts">
    import {auth} from '../../firebase-config';
    import {onMount} from 'svelte';
    import {Input, Label, Button} from 'flowbite-svelte';

    let user: any = null;
    let displayName = '';
    let email = '';

    onMount(() => {
        auth.onAuthStateChanged((currentUser) => {
            if (currentUser) {
                user = currentUser;
                displayName = currentUser.displayName || '';
                email = currentUser.email || '';
            }
        });
    });

    async function updateProfile() {
        if (user) {
            try {
                await user.updateProfile({displayName});
                await user.updateEmail(email);
                alert('Profile updated successfully!');
            } catch (error) {
                console.error('Error updating profile:', error);
                alert('Error updating profile. Please try again.');
            }
        }
    }
</script>

<h1 class="text-2xl font-bold mb-4">Profile Settings</h1>
<form on:submit|preventDefault={updateProfile} class="space-y-4">
    <div>
        <Label for="displayName" class="block text-sm font-medium text-gray-700">Display Name</Label>
        <Input id="displayName" type="text" bind:value={displayName}/>
    </div>
    <div>
        <Label for="email" class="block text-sm font-medium text-gray-700">Email</Label>
        <Input id="email" type="email" bind:value={email}/>
    </div>
    <Button type="submit"
            class="w-full bg-blue-600 text-white py-2 rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
        Update Profile
    </Button>
</form>