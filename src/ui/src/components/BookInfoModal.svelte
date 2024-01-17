<!-- modal that shows book info for a given review -->
<script lang="ts">
  import { onMount } from "svelte";
  import { api3_url } from "../config/config";

    export let review;

    onMount(() => {
        let title = review[2];
        // fetch book info from API
        fetch(`${api3_url}/book_info?title=${title}`)
            .then(async (res) => {
                if (res.status === 200) {
                    let book_info = await res.json();
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