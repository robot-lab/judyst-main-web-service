<template>
  <div id="app">
    <Navbar/>
    <Workspace/>
    <Footer/>
  </div>
</template>

<script>
import Search from './components/SearchSubcomponents/Search.vue'
import Footer from './components/Footer.vue'
import Navbar from './components/Navbar.vue'
import Workspace from './components/Workspace.vue'

import Router from './routes/router.js'

export default {
  name: 'app',
  router: Router.Router,
  components: {
    Footer,
    Navbar,
    Search,
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
