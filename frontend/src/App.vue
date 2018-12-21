<template>
  <div id="app">
    <Navbar/>
    <Workspace/>
    <Footer/>
  </div>
</template>

<script>
import Vue from 'vue';
import Router from './routes/router.js'
import Vuex from 'vuex'

import Search from './components/SearchSubcomponents/Search.vue'
import Footer from './components/Footer.vue'
import Navbar from './components/Navbar.vue'
import Workspace from './components/Workspace.vue'

import auth_store from './stores/auth_store.js'
import search_store from './stores/searchHistory_store.js'
import favorite_store from './stores/favorites_store.js'
Vue.use(Vuex);

export default {
  name: 'app',
  router: Router.Router,
  store: new Vuex.Store({
   
  
    modules:{
        auth_store,
        search_store,
        favorite_store
    }

    }),
  

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
