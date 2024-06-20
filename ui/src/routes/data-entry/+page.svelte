<script lang="ts">
    import {auth} from '../../firebase-config';
    import {signOut} from 'firebase/auth';
    import {goto} from '$app/navigation';
    import {onMount} from 'svelte';
    import {doc, setDoc, collection, getDocs} from "firebase/firestore";
    import {getFirestore} from "firebase/firestore";
    import {writable} from 'svelte/store';
    import {Accordion, AccordionItem, Button, Input, Label, Range, Select} from 'flowbite-svelte';
    import Map from "./Map.svelte";
    import SaveFields from "./SaveFields.svelte";
    import type {GeoJSON} from "leaflet";

    let currentField: any = null;
    let fieldPolygon: GeoJSON | null = null;
    const db = getFirestore();
    let authenticated = false;
    let crop = '';
    let diameterOfTreeCover: number;
    let distanceBetweenCrops: number;
    let distanceBetweenRows: number;
    let numberOfEmitters: number;
    let plotCoefficient = 0;
    let unitFlowRate: number;
    let loading = false;
    let savedFields = writable<Array<any>>([]);
    let showAdvanced = writable<boolean>(false);
    let efficiency: number = 50;
    $: irrigationEfficiency = efficiency / 100;
    let emittersPerMeter: number;
    $: numberOfEmitters = emittersPerMeter * distanceBetweenCrops;

    // New variables for WhatsApp message
    let recipientName = '';
    let recipientNumber = '';
    export let data;

    onMount(() => {
        auth.onAuthStateChanged(async (user) => {
            if (user) {
                authenticated = true;
                await fetchSavedFields(user.uid);
            } else {
                goto('/login');
            }
        });
    });

    async function fetchSavedFields(uid: string) {
        const querySnapshot = await getDocs(collection(db, "users", uid, "fields"));
        let fields: Array<any> = [];
        querySnapshot.forEach((doc) => {
            fields.push({...doc.data(), id: doc.id});
        });
        savedFields.set(fields);
    }

    async function logout() {
        await signOut(auth);
        await goto('/login');
    }

    async function handleSubmit(event: Event) {
        event.preventDefault();
        loading = true;
        try {
            const user = auth.currentUser;
            if (user) {
                const uid = user.uid;
                const fieldData = {
                    crop,
                    diameterOfTreeCover,
                    distanceBetweenCrops,
                    distanceBetweenRows,
                    irrigationEfficiency,
                    numberOfEmitters,
                    plotCoefficient,
                    unitFlowRate,
                    polygon: fieldPolygon,
                    createdAt: new Date()
                };
                
                await setDoc(doc(db, "users", uid, "fields", currentField.id), fieldData, {merge: true});
                alert('Data submitted successfully!');
                await fetchSavedFields(uid);
                await sendMessage();
                resetForm();
            }
        } catch (e) {
            console.error('Error adding document: ', e);
            alert('Error submitting data. Please try again.');
        } finally {
            loading = false;
        }
    }

    async function sendMessage() {
        const accountSid = 'your_account_sid';
        const authToken = 'your_auth_token';
        const client = require('twilio')(accountSid, authToken);

        try {
            const message = await client.messages.create({
                body: 'Your data has been submitted successfully!',
                from: '+1234567890', // TODO remove hardcode
                to: '+0987654321' // TODO add whatever number is put in here
            });
            console.log('Message sent:', message.sid);
        } catch (e) {
            console.error('Error sending message: ', e);
        }
    }

    async function sendWhatsAppMessage() {
        const accountSid = 'ACcbc5e54b47023884dde508e69bcf9ad1';
        const authToken = '39894f87671514d4b5dc307a9f5fb462';
        const client = require('twilio')(accountSid, authToken);

        try {
            const message = await client.messages.create({
                body: `Hello ${recipientName}, this is a test WhatsApp message!`,
                from: 'whatsapp:+18333687504', // Your Twilio WhatsApp number
                to: `whatsapp:${recipientNumber}`
            });
            console.log('WhatsApp message sent:', message.sid);
            alert('WhatsApp message sent successfully!');
        } catch (e) {
            console.error('Error sending WhatsApp message: ', e);
            alert('Error sending WhatsApp message. Please try again.');
        }
    }

    function toggleAdvanced() {
        showAdvanced.update(n => !n);
    }

    function handlePolygonUpdate(event: CustomEvent) {
        fieldPolygon = event.detail.polygon;
        if (currentField) {
            currentField.polygon = fieldPolygon;
        }
    }


    function resetForm() {
        currentField = null;
        fieldPolygon = null;
        crop = '';
        diameterOfTreeCover = 0;
        distanceBetweenCrops = 0;
        distanceBetweenRows = 0;
        efficiency = 50;
        emittersPerMeter = 0;
        unitFlowRate = 0;
    }

    function editField(field: any) {
        currentField = field;
        crop = field.crop;
        diameterOfTreeCover = field.diameterOfTreeCover;
        distanceBetweenCrops = field.distanceBetweenCrops;
        distanceBetweenRows = field.distanceBetweenRows;
        efficiency = field.irrigationEfficiency * 100;
        emittersPerMeter = field.numberOfEmitters / field.distanceBetweenCrops;
        unitFlowRate = field.unitFlowRate;
        fieldPolygon = field.polygon;
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

    .input-container {
        justify-content: space-between;
        display: flex;
        align-items: center;
    }

    .border {
        border: 1px solid #ccc;
    }
</style>

{#if authenticated}
    <main class="p-8 mx-auto bg-white rounded-lg shadow-md">
        <div class="flex">
            <div class="w-1/4 pr-4">
                <h2 class="text-xl font-bold mb-4">Saved Fields</h2>
                <Accordion>
                    {#each $savedFields as field, index}
                        <AccordionItem>
                <span slot="header" class="accordion-button">
                    Crop: {field.crop}
                </span>
                            <div class="accordion-body">
                                <p><strong>Diameter of Tree Cover:</strong> {field.diameterOfTreeCover}</p>
                                <p><strong>Distance Between Crops:</strong> {field.distanceBetweenCrops}</p>
                                <p><strong>Distance Between Rows:</strong> {field.distanceBetweenRows}</p>
                                <p><strong>Irrigation Efficiency:</strong> {field.irrigationEfficiency}</p>
                                <p><strong>Number of Emitters:</strong> {field.numberOfEmitters}</p>
                                <p><strong>Plot Coefficient:</strong> {field.plotCoefficient}</p>
                                <p><strong>Unit Flow Rate:</strong> {field.unitFlowRate}</p>
                            </div>
                        </AccordionItem>
                    {/each}
                </Accordion>
            </div>
            <div class="w-3/4 pl-4">
                <h1 class="text-2xl font-bold mb-4">Data Entry</h1>
                <form on:submit={handleSubmit} class="space-y-4">
                    <div>
                        <Label for="crop" class="block text-sm font-medium text-gray-700">Crop (e.g., Ciruelo)</Label>
                        <Select id="crop" bind:value={crop}
                                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            {#each data.crops as crop}
                                <option>{crop}</option>
                            {/each}
                        </Select>
                    </div>
                    <div class="input-container">
                        <label for="meterInput">Diameter of tree cover (meters):</label>
                        <Input placeholder="0" bind:value={diameterOfTreeCover} id="meterInput" type="number" min="0"
                               max="20"
                               step="0.5"
                               class="w-16 mt-1 border"/>
                    </div>
                    <div class="input-container">
                        <label for="meterInput">Distance between rows (meters):</label>
                        <Input placeholder="0" bind:value={distanceBetweenRows} id="meterInput" type="number" min="0"
                               max="20"
                               step="0.5"
                               class="w-16 mt-1 border"/>
                    </div>
                    <div class="input-container">
                        <label for="meterInput">Distance between trees (meters):</label>
                        <Input placeholder="0" bind:value={distanceBetweenCrops} id="meterInput" type="number" min="0"
                               max="20"
                               step="0.5"
                               class="w-16 mt-1 border"/>
                    </div>
                    <div class="input-container">
                        <label for="meterInput">Irrigation Efficiency:</label>
                        {#if !$showAdvanced}
                            <div class:showAdvanced={false}>
                                <Button class="w-16" size="xs" outline color="blue" type="button"
                                        on:click={() => efficiency=80}>Sprinkler
                                    (80%)
                                </Button>
                                <Button class="w-16" size="xs" outline color="green" type="button"
                                        on:click={() => efficiency=95}>Drip
                                    (95%)
                                </Button>
                            </div>
                            <Button color="none" outline size="sm" type="button" on:click={toggleAdvanced}>Advanced
                            </Button>
                        {/if}


                        {#if $showAdvanced}
                            <Range size="sm" min="0" max="100" bind:value={efficiency} step="5"/>
                            <p>{efficiency} %</p>
                            <Button color="none" size="sm" type="button" on:click={toggleAdvanced}>Standard</Button>
                        {/if}
                    </div>

                    <div class="input-container">
                        <label for="meterInput">Irrigation Emitters per meter:</label>
                        <Input placeholder="0" bind:value={emittersPerMeter} id="meterInput" type="number" min="0"
                               max="20"
                               step="1"
                               class="w-16 mt-1 border"/>
                    </div>
                    <div class="input-container">
                        <label for="meterInput">Flow Rate per Emitter (L/h):</label>
                        <Input placeholder="0" bind:value={unitFlowRate} id="meterInput" type="number" min="0" max="200"
                               step="10"
                               class="w-16 mt-1 border"/>
                    </div>
                    <div>
                        <Map initialPolygon={fieldPolygon} on:polygonUpdated={handlePolygonUpdate}/>
                    </div>

                    <Button outline type="submit"
                            class="w-full bg-indigo-600 text-white py-2 rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        {currentField ? 'Update' : 'Submit'}
                    </Button>
                </form>
                {#if loading}
                    <div class="flex justify-center mt-4">
                        <div class="spinner"></div>
                    </div>
                {/if}
                <Button on:click={logout}
                        class="mt-4 w-full bg-red-600 text-white py-2 rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                    Logout
                </Button>

                <!-- New section for sending WhatsApp message -->
                <section class="mt-8">
                    <h2 class="text-xl font-bold mb-4">Send WhatsApp Message</h2>
                    <div class="space-y-4">
                        <div>
                            <label for="recipientName" class="block text-sm font-medium text-gray-700">Recipient
                                Name</label>
                            <input id="recipientName" type="text" bind:value={recipientName}
                                   class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"/>
                        </div>
                        <div>
                            <label for="recipientNumber" class="block text-sm font-medium text-gray-700">Recipient
                                Number (with
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
            </div>
        </div>
    </main>
{:else}
    <p>Loading...</p>
{/if}
