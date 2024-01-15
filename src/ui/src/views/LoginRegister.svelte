<script lang="ts">
  import {
    Container,
    Row,
    Col,
    Form,
    FormGroup,
    Label,
    Input,
    Button,
    Alert
  } from '@sveltestrap/sveltestrap';

  import { loged_user } from '../stores/usersStore';

  import { fade } from 'svelte/transition';

  import {api_url} from '../config/config';

  let username = '';
  let password = '';
  let showError = false;
  let errorMessage = '';

  const handleLogin = async () => {
    // prevent default form submission
    event.preventDefault();

    // Send login request to API
    const response = await fetch(`${api_url}/LoginRegisterService/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        password
      })
    }).then(async res => {
        if (res.status === 200) {
            showError = false;
            // redirect to home page
            let user = await res.json();
            loged_user.set(user)
            window.location.href = '#/home';
        } else if (res.status === 503) {
            showError = true;
            errorMessage = 'Service unavailable. Please try again later.';
        } 
        else {
            showError = true;
            errorMessage = 'Invalid username or password. Please try again.';
        }
        }).catch(err => {
        console.log(err);
    });
  };
</script>

<Container class="mt-5">
  <Row>
    <Col md="20" class="mx-auto">
      {#if showError}
        <div transition:fade="{{ duration: 300 }}">
          <Alert color="danger">
            {errorMessage}
          </Alert>
        </div>
      {/if}

      <Form>
        <FormGroup>
          <Label for="username">Username:</Label>
          <Input type="text" id="username" bind:value={username} placeholder="Enter your username" required />
        </FormGroup>

        <FormGroup>
          <Label for="password">Password:</Label>
          <Input type="password" id="password" bind:value={password} placeholder="Enter your password" required />
        </FormGroup>

        <Button color="primary" block on:click={handleLogin}>Login</Button>
      </Form>

      <p class="mt-3 text-center">
        Don't have an account? <a on:click={() => console.log('Navigate to register page')}>Register here</a>.
      </p>
    </Col>
  </Row>
</Container>
