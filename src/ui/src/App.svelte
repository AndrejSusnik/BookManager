<script>
  import { Styles } from '@sveltestrap/sveltestrap';
  import { Button, Col, Row } from '@sveltestrap/sveltestrap';
  import Router from 'svelte-spa-router';
  import LoginRegister from './views/LoginRegister.svelte';
  import Home from './views/Home.svelte';
  import Settings from './views/Settings.svelte';
  import Stats from './views/Stats.svelte';

  const routes = {
    '/': LoginRegister,
    '/settings': Settings,
    '/home': Home,
    '/stats': Stats,
  }

</script>

<svelte:head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</svelte:head>

<main>
  <Styles />
  <Router {routes}/>
</main>

<style>
  @import 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css';
</style>
