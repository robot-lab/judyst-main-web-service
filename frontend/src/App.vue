<template>
  <div id="app">
    <Navbar/>
    <Workspace/>
    <Footer/>
  </div>
</template>

<script>
import LinkSearch from './components/LinkSearch.vue'
import Footer from './components/Footer.vue'
import Navbar from './components/Navbar.vue'
import Workspace from './components/Workspace.vue'
export default {
  name: 'app',
  components: {
    Footer,
    Navbar,
    LinkSearch,
    Workspace
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
