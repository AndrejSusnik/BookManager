<script lang="ts">
  import { api2_url } from "../config/config";
  export let review;
  export let deleted_callback = (review) => {};
  import { fade } from "svelte/transition";

  import {
    Card,
    Alert,
    CardBody,
    CardTitle,
    CardText,
    Styles,
    Button,
    CardHeader,
    Container,
    Col,
    Row,
    CardFooter,
  } from "@sveltestrap/sveltestrap";

  let showError = false;
  let errorMessage = "";

  let format_rating = (rating: string) => {
    let rating_num = parseFloat(rating);

    return rating_num.toFixed(2);
  };

  let delete_review = (review) => {
    fetch(`${api2_url}/book_review`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: review[0],
        user_id: review[1],
      }),
    })
      .then(async (res) => {
        if (res.status === 200) {
          deleted_callback(review);
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
  };
</script>

<main>
  <Card>
    <CardBody>
      <CardHeader>
        <Row>
          <Col>
            <CardTitle>{review[2]}</CardTitle>
          </Col>
          <Col>
            <Button
              color="danger"
              on:click={() => {
                delete_review(review);
                deleted_callback(review);
              }}
            >
              Delete
            </Button>
          </Col>
        </Row>
      </CardHeader>
      <CardBody>
        <CardText>Review: {review[3]}</CardText>
        <CardText>Rating: {review[4]} / 10</CardText>
        <CardText>Time spent: {format_rating(review[5])} h</CardText>
      </CardBody>
    </CardBody>
    <CardFooter>
      {#if showError}
        <div transition:fade="{{ duration: 300 }}">
          <Alert color="danger">
            {errorMessage}
          </Alert>
        </div>
      {/if}
    </CardFooter>
  </Card>
</main>
