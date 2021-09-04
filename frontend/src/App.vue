<template>
  <Navbar />
  <Board />
</template>

<script>
import Board from "./components/Board.vue";
import Navbar from "./components/Navbar.vue";

export default {
  name: "App",
  components: {
    Board,
    Navbar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
