<!-- modal that shows book info for a given review -->
<script lang="ts">
  import { onMount } from "svelte";
  import { api3_url } from "../config/config";

  import {
    Modal,
    ModalHeader,
    ModalBody,
    ModalFooter,
    Button,
  } from "@sveltestrap/sveltestrap";

  export let modalOpen = false;
  export let review;

  function toggleModal() {
    modalOpen = !modalOpen;
  }

  class BookInfo {
    book_id: string;
    name: string;
    cover: string;
    url: string;
    authors: string[];
    rating: number;
    created_editions: number;
    year: number;
  }

  let book_info: BookInfo | null = null;

  onMount(() => {
    let title = review[2];
    fetch(`${api3_url}/get_book_info?title=${title}`)
      .then(async (res) => {
        if (res.status === 200) {
          book_info = await res.json();
          console.log(book_info);
        } else {
          console.log("Error fetching book info");
        }
      })
      .catch((err) => {
        console.log(err);
      });
  });
</script>

<main>
  <Modal bind:isOpen={modalOpen} backdrop="static">
    {#if book_info}
      <ModalHeader toggle={toggleModal}>{book_info.name}</ModalHeader>
      <ModalBody>
        <dl class="row">
          {#if book_info.cover}
            <dt class="col-sm-3">Cover</dt>
            <dd class="col-sm-9">
              <img src={book_info.cover} alt="cover" width="100" height="100" />
            </dd>
          {/if}

          <dt class="col-sm-3">Title</dt>
          <dd class="col-sm-9">{book_info.name}</dd>

          <dt class="col-sm-3">Authors</dt>
          <dd class="col-sm-9">{book_info.authors.join(", ")}</dd>

          <dt class="col-sm-3">Average rating</dt>
          <dd class="col-sm-9">{book_info.rating} / 5</dd>
          <dt class="col-sm-3">Your rating</dt>
          <dd class="col-sm-9">{review[4]} / 10</dd>

          <dt class="col-sm-3">Created Editions</dt>
          <dd class="col-sm-9">{book_info.created_editions}</dd>

          <dt class="col-sm-3">Year</dt>
          <dd class="col-sm-9">{book_info.year}</dd>
        </dl>
      </ModalBody>
    {:else}
      <p>Loading book info...</p>
    {/if}
    <ModalFooter>
      <Button color="secondary" on:click={toggleModal}>Close</Button>
    </ModalFooter>
  </Modal>
</main>
