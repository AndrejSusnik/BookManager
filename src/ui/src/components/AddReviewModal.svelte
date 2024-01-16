<script lang="ts">
    import {Alert, Button, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Label, Input, Row, Col } from '@sveltestrap/sveltestrap';
  export let closeCallback;
  export let review_added_callback = (review) => {};
  import {api2_url} from '../config/config';
  import { loged_user } from '../stores/usersStore';
  import { fade } from 'svelte/transition';

  export let modalOpen = false;

  function toggleModal() {
    modalOpen = !modalOpen;
  }

  let bookName = "";
  let review = "";
  let rating = "";
  let hoursSpent = "";

  let showError = false;
  let errorMessage = '';


  function handleFormSubmit() {
    // Close the modal after handling form submission
    toggleModal();
    event.preventDefault();

    // send review to API
    fetch(`${api2_url}/BookManagerService/book_review`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: 0,
        user_id: $loged_user[0],
        title: bookName,
        review: review,
        rating: rating,
        time_spent: hoursSpent
      })
    }).then(async res => {
      if (res.status === 200) {
        let review = await res.json();
        review_added_callback(review);
      } else if (res.status === 503) {
        showError = true;
        errorMessage = 'Service unavailable. Please try again later.';
      } else {
        showError = true;
        errorMessage = 'Invalid username or password. Please try again.';
      }
    }).catch(err => {
      console.log(err);
    });
  }
</script>

<main>
  <Modal bind:isOpen={modalOpen} backdrop="static">
    <ModalHeader toggle={toggleModal}>Add book review</ModalHeader>
    <ModalBody>
     <Form on:submit={handleFormSubmit}>
      <FormGroup>
        <Label for="bookName">Book Name</Label>
        <Input type="text" id="bookName" bind:value={bookName} required />
      </FormGroup>
      <FormGroup>
        <Label for="review">Review</Label>
        <Input type="textarea" id="review" bind:value={review} required />
      </FormGroup>
      <Row>
        <Col md="6">
          <FormGroup>
            <Label for="rating">Rating (out of 10)</Label>
            <Input type="number" id="rating" bind:value={rating} min="0" max="10" required />
          </FormGroup>
        </Col>
        <Col md="6">
          <FormGroup>
            <Label for="hoursSpent">Hours Spent Reading</Label>
            <Input type="number" id="hoursSpent" bind:value={hoursSpent} min="0" required />
          </FormGroup>
        </Col>
      </Row>
      <Button color="primary" type="submit">Submit</Button>
    </Form>
  </ModalBody>
  <ModalFooter>
    <Button color="secondary" on:click={toggleModal}>Close</Button>
    {#if showError}
      <div transition:fade="{{ duration: 300 }}">
        <Alert color="danger">
          {errorMessage}
        </Alert>
      </div>
    {/if}
  </ModalFooter>
  </Modal>
</main>
