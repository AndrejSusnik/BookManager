<script>
  import {
    Navbar,
    Nav,
    NavItem,
    NavLink,
    Button,
    Styles,
  } from "@sveltestrap/sveltestrap";

  import { loged_user } from "../stores/usersStore";

    const logout = () => {
        loged_user.set(null);
        window.location.href = "/";
    };

    const settings = () => {
        window.location.href = "#/settings";
    };

    const home = () => {
      console.log("home");
        window.location.href = "#/home";
    };
</script>

<main>
<Styles />
<Navbar color="light" light expand="md">
  <Nav navbar>
    <NavItem>
      <NavLink on:click={home}>Home</NavLink>
    </NavItem>
  </Nav>

  <Nav navbar>
    <NavItem>
      <NavLink on:click={settings}>Settings</NavLink>
    </NavItem>
  </Nav>

  <Nav navbar class="ml-auto">
    <NavItem>
      <span class="navbar-text">
        <Button color="link" on:click={logout}>Logout</Button>
      </span>
    </NavItem>
  </Nav>
</Navbar>
</main>

<style>
  /* You can add your custom styling here */
</style>
