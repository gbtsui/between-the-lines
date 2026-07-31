<script lang="ts">
    import './layout.css';
    import favicon from '$lib/assets/favicon.svg';
    import "@fontsource/noto-serif"
    //import {resolve} from "$app/paths";


    let { children } = $props();
</script>

<style>
    :global(body) {
        font-family: "Noto Serif", serif
    }
</style>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}
