<script>
    export let addClickedCallback = () => {console.log("default");};
  import { Card, CardBody } from '@sveltestrap/sveltestrap';
</script>

<style>
  .card-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px; /* Adjust the height as needed */
  }

  .plus-icon {
    font-size: 4em;
    cursor: pointer;
    transition: color 0.3s ease;
    color: black;
  }
</style>

<Card>
  <CardBody class="card-container">
    <div class="plus-icon" on:click={addClickedCallback}>
      +
    </div>
    <h5 class="card-title">To add a review click on the +</h5>
  </CardBody>
</Card>
