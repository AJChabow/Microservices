<script lang="ts">
    import {onMount} from 'svelte';
    import {writable} from 'svelte/store';
    import {collection, getDocs} from "firebase/firestore";
    import {getFirestore} from "firebase/firestore";
    import {Accordion, AccordionItem} from 'flowbite-svelte';

    const db = getFirestore();
    let savedFields = writable<Array<any>>([]);

    // Fetch the saved fields from Firestore
    async function fetchSavedFields(uid: string) {
        const querySnapshot = await getDocs(collection(db, "users", uid, "fields"));
        let fields: Array<any> = [];
        querySnapshot.forEach((doc) => {
            fields.push({...doc.data(), id: doc.id});
        });
        savedFields.set(fields);
    }

    // Simulate authenticated state and fetch data (replace this with real auth check)
    let authenticated = true;
    onMount(async () => {
        if (authenticated) {
            // Replace 'user-uid' with the actual user UID
            await fetchSavedFields('user-uid');
        }
    });
</script>


