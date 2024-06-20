<!-- src/routes/whatsapp/+page.svelte -->
<script lang="ts">
    import {Button, Input, Label} from 'flowbite-svelte';

    let recipientName = '';
    let recipientNumber = '';

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
</script>

<h1 class="text-2xl font-bold mb-4">Send WhatsApp Message</h1>
<div class="space-y-4">
    <div>
        <Label for="recipientName" class="block text-sm font-medium text-gray-700">Recipient Name</Label>
        <Input id="recipientName" type="text" bind:value={recipientName}/>
    </div>
    <div>
        <Label for="recipientNumber" class="block text-sm font-medium text-gray-700">Recipient Number (with country
            code, e.g., +1234567890)</Label>
        <Input id="recipientNumber" type="text" bind:value={recipientNumber}/>
    </div>
    <Button on:click={sendWhatsAppMessage}
            class="w-full bg-green-600 text-white py-2 rounded-md shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        Send WhatsApp Message
    </Button>
</div>