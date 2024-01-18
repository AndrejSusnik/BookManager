<script lang="ts">
  import {
    Alert,
    Button,
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Form,
    FormGroup,
    Label,
    Input,
    Row,
    Col,
  } from "@sveltestrap/sveltestrap";
  export let review_added_callback = (review) => {};
  import { api2_url, api3_url } from "../config/config";
  import { loged_user } from "../stores/usersStore";
  import { fade } from "svelte/transition";
  import { onMount } from "svelte";

  export let modalOpen = false;

  function toggleModal() {
    modalOpen = !modalOpen;
  }

  let bookName = "";
  let review = "";
  let rating = "";
  let hoursSpent = "";

  let showError = false;
  let errorMessage = "";

  function handleFormSubmit() {
    // Close the modal after handling form submission
    toggleModal();
    event.preventDefault();

    // send review to API
    fetch(`${api2_url}/book_review`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: 0,
        user_id: $loged_user[0],
        title: bookName,
        review: review,
        rating: rating,
        time_spent: hoursSpent,
      }),
    })
      .then(async (res) => {
        if (res.status === 200) {
          let review = await res.json();
          review_added_callback(review);
        } else if (res.status === 503) {
          showError = true;
          errorMessage = "Service unavailable. Please try again later.";
        } else {
          showError = true;
          errorMessage = "Invalid username or password. Please try again.";
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }

  let last_keypress = 0;
  let last_fetch = Date.now();

  let suggestions = [];

  let get_suggestions = (partial: String) => {
    if (partial.length > 5) {
      if (Date.now() - last_keypress > 500 && Date.now() - last_fetch > 500) {
        // fetch suggestions
        fetch(`${api3_url}/get_name_completion_list?partial=${partial}`)
          .then(async (res) => {
            if (res.status === 200) {
              let completions = await res.json();
              suggestions = completions.completions;

              // filter out duplicates from suggestions
              suggestions = suggestions.filter(
                (suggestion, index, self) => self.indexOf(suggestion) === index
              );
            } else if (res.status === 503) {
              showError = true;
              errorMessage = "Service unavailable. Please try again later.";
            } else {
              showError = true;
              errorMessage = "Invalid username or password. Please try again.";
            }
          })
          .catch((err) => {
            console.log(err);
          });
        // update last fetch time
        last_fetch = Date.now();
      }
    }
  };
</script>

<main>
  <Modal bind:isOpen={modalOpen} backdrop="static">
    <ModalHeader toggle={toggleModal}>Add book review</ModalHeader>
    <ModalBody>
      <Form on:submit={handleFormSubmit}>
        <FormGroup>
          <Label for="bookName">Book Name</Label>
          <Input
            list="book-names"
            type="text"
            id="bookName"
            bind:value={bookName}
            on:keyup={() => {
              last_keypress = Date.now();
              setTimeout(() => get_suggestions(bookName), 1000);
            }}
            required
          />
          <datalist id="book-names">
            {#each suggestions as suggestion (suggestion)}
              <option value={suggestion}>{suggestion}</option>
            {/each}
          </datalist>
        </FormGroup>
        <FormGroup>
          <Label for="review">Review</Label>
          <Input type="textarea" id="review" bind:value={review} required />
        </FormGroup>
        <Row>
          <Col md="6">
            <FormGroup>
              <Label for="rating">Rating (out of 10)</Label>
              <Input
                type="number"
                id="rating"
                bind:value={rating}
                min="0"
                max="10"
                required
              />
            </FormGroup>
          </Col>
          <Col md="6">
            <FormGroup>
              <Label for="hoursSpent">Hours Spent Reading</Label>
              <Input
                type="number"
                id="hoursSpent"
                bind:value={hoursSpent}
                min="0"
                required
              />
            </FormGroup>
          </Col>
        </Row>
        <Button color="primary" type="submit">Submit</Button>
      </Form>
    </ModalBody>
    <ModalFooter>
      <Button color="secondary" on:click={toggleModal}>Close</Button>
      {#if showError}
        <div transition:fade={{ duration: 300 }}>
          <Alert color="danger">
            {errorMessage}
          </Alert>
        </div>
      {/if}
    </ModalFooter>
  </Modal>
</main>
