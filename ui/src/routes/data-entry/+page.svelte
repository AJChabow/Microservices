<script lang="ts">
  import { auth } from '../../firebase-config';
  import { signOut } from 'firebase/auth';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { doc, setDoc } from "firebase/firestore";
  import { getFirestore } from "firebase/firestore";
  const db = getFirestore();
  let authenticated = false;
  let crop = '';
  let diameterOfTreeCover = '';
  let distanceBetweenCrops = '';
  let distanceBetweenRows = '';
  let installationEfficiency = '';
  let numberOfEmitters = '';
  let plotCoefficient = '';
  let unitFlowRate = '';
  let loading = false;

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
    await goto('/login');
  }

  async function handleSubmit(event: any) {
    event.preventDefault();
    loading = true;
    try {
      await setDoc(doc(db, "users", 'Farming-Field'), {
        crop,
        diameterOfTreeCover,
        distanceBetweenCrops,
        distanceBetweenRows,
        installationEfficiency,
        numberOfEmitters,
        plotCoefficient,
        unitFlowRate,
        createdAt: new Date()
      });
      alert('Data submitted successfully!');
      // Reset the form
      crop = '';
      diameterOfTreeCover = '';
      distanceBetweenCrops = '';
      distanceBetweenRows = '';
      installationEfficiency = '';
      numberOfEmitters = '';
      plotCoefficient = '';
      unitFlowRate = '';
    } catch (e) {
      console.error('Error adding document: ', e);
      alert('Error submitting data. Please try again.');
    } finally {
      loading = false;
    }
  }
</script>

<style>
  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #4F46E5;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>

{#if authenticated}
  <main class="p-8 max-w-md mx-auto bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-4">Data Entry</h1>
    <form on:submit={handleSubmit} class="space-y-4">
      <div>
        <label for="crop" class="block text-sm font-medium text-gray-700">Crop</label>
        <input id="crop" type="text" bind:value={crop} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="diameterOfTreeCover" class="block text-sm font-medium text-gray-700">Diameter of Tree Cover</label>
        <input id="diameterOfTreeCover" type="text" bind:value={diameterOfTreeCover} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="distanceBetweenCrops" class="block text-sm font-medium text-gray-700">Distance Between Crops</label>
        <input id="distanceBetweenCrops" type="text" bind:value={distanceBetweenCrops} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="distanceBetweenRows" class="block text-sm font-medium text-gray-700">Distance Between Rows</label>
        <input id="distanceBetweenRows" type="text" bind:value={distanceBetweenRows} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="installationEfficiency" class="block text-sm font-medium text-gray-700">Installation Efficiency</label>
        <input id="installationEfficiency" type="text" bind:value={installationEfficiency} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="numberOfEmitters" class="block text-sm font-medium text-gray-700">Number of Emitters</label>
        <input id="numberOfEmitters" type="text" bind:value={numberOfEmitters} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="plotCoefficient" class="block text-sm font-medium text-gray-700">Plot Coefficient</label>
        <input id="plotCoefficient" type="text" bind:value={plotCoefficient} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <div>
        <label for="unitFlowRate" class="block text-sm font-medium text-gray-700">Unit Flow Rate</label>
        <input id="unitFlowRate" type="text" bind:value={unitFlowRate} class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
      <button type="submit" class="w-full bg-indigo-600 text-white py-2 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Submit</button>
    </form>
    {#if loading}
      <div class="flex justify-center mt-4">
        <div class="spinner"></div>
      </div>
    {/if}
    <button on:click={logout} class="mt-4 w-full bg-red-600 text-white py-2 rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">Logout</button>
  </main>
{:else}
  <p>Loading...</p>
{/if}
