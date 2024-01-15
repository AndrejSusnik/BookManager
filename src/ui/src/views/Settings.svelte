<script>
  import { Form, FormGroup, Label, Input, Button } from '@sveltestrap/sveltestrap';
  import Navbar from '../components/Navbar.svelte';

  let username = '';
  let password = '';
  let confirmPassword = '';

  function handleChange() {
    // You can perform validation and send the data to the server here
    console.log('Username:', username);
    console.log('Password:', password);
    console.log('Confirm Password:', confirmPassword);

    // Reset fields after handling data
    username = '';
    password = '';
    confirmPassword = '';
  }
</script>

<main>
    <Navbar/>
  <h2 class="mb-4">Change User Parameters</h2>

  <!-- <Form on:submit|preventDefault={handleChange}>
    <FormGroup>
      <Label for="username">Username:</Label>
      <Input type="text" id="username" bind:value={username} />
    </FormGroup>

    <FormGroup>
      <Label for="password">Password:</Label>
      <Input type="password" id="password" bind:value={password} />
    </FormGroup>

    <FormGroup>
      <Label for="confirmPassword">Confirm Password:</Label>
      <Input type="password" id="confirmPassword" bind:value={confirmPassword} />
    </FormGroup>

    <Button color="primary" type="submit">Submit</Button>
  </Form> -->
</main>

<style>
  /* You can add your custom styling here */
</style>
