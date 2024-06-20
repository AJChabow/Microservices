<!-- src/routes/+layout.svelte -->
<script lang="ts">
    import {onMount} from 'svelte';
    import "../app.css";
    import {goto} from '$app/navigation';
    import {auth} from '../firebase-config';
    import {
        Navbar,
        NavBrand,
        NavHamburger,
        NavUl,
        NavLi,
        Sidebar,
        SidebarGroup,
        SidebarItem,
        SidebarWrapper,
        Button
    } from 'flowbite-svelte';
    import {UserCircle} from 'svelte-heros-v2';
    import {page} from '$app/stores';

    let authenticated = false;

    onMount(async () => {
        auth.onAuthStateChanged((user) => {
            if (user) {
                authenticated = true;
            } else {
                authenticated = false;
                goto('/login');
            }
        });
    });

    async function logout() {
        await auth.signOut();
        await goto('/login');
    }
</script>

{#if authenticated}
    <Navbar let:hidden let:toggle>
        <NavBrand href="/">
            <img src="src/lib/images/cropmind_logo.png" class="mr-3 h-6 sm:h-9" alt="Cropmind logo"/>
        </NavBrand>
        <div class="flex md:order-2">
            <Button color="light" class="mr-2" href="/profile">
                <UserCircle class="mr-2 h-5 w-5"/>
                Profile
            </Button>
            <Button color="red" on:click={logout}>Logout</Button>
            <NavHamburger on:click={toggle}/>
        </div>
        <NavUl {hidden}>
            <NavLi href="/data-entry" active={$page.url.pathname === '/data-entry'}>Data Entry</NavLi>
            <NavLi href="/fields" active={$page.url.pathname === '/fields'}>Fields</NavLi>
            <NavLi href="/whatsapp" active={$page.url.pathname === '/whatsapp'}>Whatsapp</NavLi>
        </NavUl>
    </Navbar>

    <div class="flex">
        <main class="flex-1 p-4 pt-20">
            <slot/>
        </main>
    </div>
{:else}
    <slot/>
{/if}