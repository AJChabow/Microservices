<script lang="ts">
    import {auth} from '../../firebase-config';
    import {signOut} from 'firebase/auth';
    import {goto} from '$app/navigation';
    import {onMount} from 'svelte';
    import {doc, setDoc} from "firebase/firestore";
    import {getFirestore} from "firebase/firestore";

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
    export let data

    // New variables for WhatsApp message
    let recipientName = '';
    let recipientNumber = '';

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

    async function sendWhatsAppMessage() {
        const accountSid = 'ACcbc5e54b47023884dde508e69bcf9ad1';
        const authToken = '39894f87671514d4b5dc307a9f5fb462';
        const client = require('twilio')(accountSid, authToken);

        try {
            const message = await client.messages.create({
                body: `Hello ${recipientName}, this is a test WhatsApp message!`,
                from: 'whatsapp:+18333687504', // Your Twilio WhatsApp number TODO remove hardcode
                to: `whatsapp:${recipientNumber}`
            });
            console.log('WhatsApp message sent:', message.sid);
            alert('WhatsApp message sent successfully!');
        } catch (e) {
            console.error('Error sending WhatsApp message: ', e);
            alert('Error sending WhatsApp message. Please try again.');
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
        <h1 class="text-2xl font-bold mb-4">Edit Field</h1>
        <form on:submit={handleSubmit} class="space-y-4">
            <div>

                <label for="crop" class="block text-sm font-medium text-gray-700">Crop (e.g., Ciruelo)</label>
                <select bind:value={crop} class="border-gray-400 border-2 rounded-md">
                    {#each data.crops as crop, i}
                        <option class="block text-sm font-medium text-gray-700">
                            {crop}
                        </option>
                    {/each}
                </select>
            </div>

            <div>
                <label for="diameterOfTreeCover" class="block text-sm font-medium text-gray-700">Diameter of Tree Cover
                    (meters)</label>
                <input id="diameterOfTreeCover" type="number" bind:value={diameterOfTreeCover} max="30" min="0"
                       step="0.5"
                       class="max-w-10  mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"/>
            </div>
            <div>
                <span
                        for="distanceBetweenCrops" class="block text-sm font-medium text-gray-700">Distance Between Crops
                    (meters)</span>
                <input id="distanceBetweenCrops" type="number" bind:value={distanceBetweenCrops} max="30" min="0"
                       step="0.5"
                       class=" max-w-10 mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"/>
            </div>
            <div>
                <label for="distanceBetweenRows" class="block text-sm font-medium text-gray-700">Distance Between Rows
                    (meters)</label>
                <input id="distanceBetweenRows" type="text" bind:value={distanceBetweenRows}
                       class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"/>
            </div>
            <div>
                <label for="installationEfficiency" class="block text-sm font-medium text-gray-700">Installation
                    Efficiency (0-1)</label>
                <input id="installationEfficiency" type="text" bind:value={installationEfficiency}
                       class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"/>
            </div>
            <div>
                <label for="numberOfEmitters" class="block text-sm font-medium text-gray-700">Number of Emitters</label>
                <input id="numberOfEmitters" type="text" bind:value={numberOfEmitters}
                       class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"/>
            </div>
            <div>
                <label for="plotCoefficient" class="block text-sm font-medium text-gray-700">Plot Coefficient
                    (0-1)</label>
                <input id="plotCoefficient" type="text" bind:value={plotCoefficient}
                       class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"/>
            </div>
            <div>
                <label for="unitFlowRate" class="block text-sm font-medium text-gray-700">Unit Flow Rate
                    (liters/hour)</label>
                <input id="unitFlowRate" type="text" bind:value={unitFlowRate}
                       class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm sm:text-sm"/>
            </div>
            <button type="submit"
                    class="w-full bg-indigo-600 text-white py-2 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2">
                Submit
            </button>
        </form>
        {#if loading}
            <div class="flex justify-center mt-4">
                <div class="spinner"></div>
            </div>
        {/if}
        <button on:click={logout}
                class="mt-4 w-full bg-red-600 text-white py-2 rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
            Logout
        </button>

        <!-- New section for sending WhatsApp message -->
        <section class="mt-8">
            <h2 class="text-xl font-bold mb-4">Send WhatsApp Message</h2>
            <div class="space-y-4">
                <div>
                    <label for="recipientName" class="block text-sm font-medium text-gray-700">Recipient Name</label>
                    <input id="recipientName" type="text" bind:value={recipientName}
                           class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"/>
                </div>
                <div>
                    <label for="recipientNumber" class="block text-sm font-medium text-gray-700">Recipient Number (with
                        country code, e.g., +1234567890)</label>
                    <input id="recipientNumber" type="text" bind:value={recipientNumber}
                           class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"/>
                </div>
                <button on:click={sendWhatsAppMessage}
                        class="w-full bg-green-600 text-white py-2 rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                    Send WhatsApp Message
                </button>
            </div>
        </section>
    </main>
{:else}
    <p>Loading...</p>
{/if}
