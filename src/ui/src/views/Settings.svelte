<script lang="ts">
  import { Button, Container, Input } from "@sveltestrap/sveltestrap";
  import Navbar from "../components/Navbar.svelte";
  import { api_url } from "../config/config";

  let etcdValue = "";
  let etcdKey = "";
  let configValue = "";
  let configKey = "";

  let disable_database = () => {
    fetch(`${api_url}/health/disable_db`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
      })
      .catch((err) => console.error(err));
  };

  let invalidate_database = () => {
    fetch(`${api_url}/health/invalidate_db_connection`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
      })
      .catch((err) => console.error(err));
  };

  let get_etcd_value = () => {
    fetch(`${api_url}/etcd_demo/etcd?path=` + etcdKey, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((res) => {
        etcdValue = res.value;
      })
      .catch((err) => console.error(err));
  };

  let set_etcd_value = () => {
    fetch(`${api_url}/etcd_demo/etcd`, {
      method: "POST",
      body: JSON.stringify({
        path: etcdKey,
        value: etcdValue,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
      })
      .catch((err) => console.error(err));
  };

  let delete_etcd_value = () => {
    fetch(`${api_url}/etcd_demo/etcd`, {
      method: "DELETE",
      body: JSON.stringify({
        path: etcdKey,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
      })
      .catch((err) => console.error(err));
  };

  let get_config_value = () => {
    fetch(`${api_url}/etcd_demo/config?key=` + configKey, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((res) => {
        configValue = res.value;
      })
      .catch((err) => console.error(err));
  };
</script>

<main>
  <Navbar />
  <h1>Settings</h1>
  <h2>Liveness check and fault tolerance check</h2>
  <Button color="primary" on:click={disable_database}>Disable database</Button>
  <Button color="primary" on:click={invalidate_database}
    >Corrupt database connection</Button
  >

  <h2>Etcd test</h2>
  <Input type="text" bind:value={etcdKey} placeholder="Etcd key" />
  <Input type="text" bind:value={etcdValue} placeholder="Etcd value" />
  <Button style="margin-bottom: 20px" on:click={get_etcd_value} color="primary">Get value</Button>
  <Button style="margin-bottom: 20px" on:click={set_etcd_value} color="secondary">Set value</Button>
  <Button style="margin-bottom: 20px" on:click={delete_etcd_value} color="danger">Delete value</Button>

  <Input type="text" bind:value={configKey} placeholder="Config key" />
  <Input type="text" bind:value={configValue} disabled placeholder="Config value" />
  <Button color="primary" on:click={get_config_value}>Get config value</Button>
</main>
