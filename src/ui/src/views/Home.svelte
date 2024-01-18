<script lang="ts">
  import Navbar from "../components/Navbar.svelte";
  import { loged_user } from "../stores/usersStore";
  import Review from "../components/Review.svelte";
  import { onMount } from "svelte";
  import { api2_url } from "../config/config";
  import { Container, Row, Col } from "@sveltestrap/sveltestrap";
  import AddReviewCard from "../components/AddReviewCard.svelte";
  import AddReviewModal from "../components/AddReviewModal.svelte";
  import BookInfoModal from "../components/BookInfoModal.svelte";

  let reviews = [];

  onMount(async () => {
    // get all reveiws from API
    console.log($loged_user);
    if ($loged_user == null) {
      window.location.href = "/";
    } else {
      // fetch book reviews for user from API
      let response = await fetch(
        `${api2_url}/book_reviews?user_id=${$loged_user[0]}`
      )
        .then((res) => res.json())
        .then((data) => {
          reviews = data;
        })
        .catch((err) => {
          console.log(err);
        });
    }
  });

  let show_add_review_modal = false;
  let openModal = () => {
    show_add_review_modal = true;
  };

  let show_book_info_modal = false;
  let openBookInfoModal = () => {
    show_book_info_modal = true;
  };
  let reviewInfo = null;

  let on_title_clicked = (review) => {
    reviewInfo = review;
    openBookInfoModal();
  };

  let review_added_callback = (review) => {
    reviews = [...reviews, review];
  };

  let review_deleted_callback = (review) => {
    reviews = reviews.filter((r) => r[0] !== review[0]);
  };
</script>

<main>
  <Navbar />
  <Row>
    {#each reviews as review}
      <Col xs="12" sm="6" md="4" lg="3" xl="3">
        <Container>
          <Review {review} deleted_callback="{review_deleted_callback}" on_title_clicked="{on_title_clicked}"/>
        </Container>
      </Col>
    {/each}
    <Col xs="12" sm="6" md="4" lg="3" xl="3">
      <Container>
        <AddReviewCard addClickedCallback="{openModal}"/>
      </Container>
    </Col>
  </Row>

  {#if show_add_review_modal}
    <AddReviewModal
      bind:modalOpen="{show_add_review_modal}"
      review_added_callback="{review_added_callback}"
    />
  {/if}

  {#if show_book_info_modal}
    <BookInfoModal
      bind:modalOpen="{show_book_info_modal}"
      review="{reviewInfo}"
    />
  {/if} 
</main>
