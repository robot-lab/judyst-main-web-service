<template>
<nav class="navbar fixed-top navbar-dark bg-dark  navbar-main">
        <div class="container-fluid">
          <div class="navbar-header">
            <router-link :to="'/'" class="navbar-brand">Judyst</router-link>
          </div>
          <b-navbar-nav left>
            <b-nav-item :to="'/search/'">Search</b-nav-item>
          </b-navbar-nav> 
          <b-navbar-nav>
            <auth-bar/>
          </b-navbar-nav>

        
        </div><!--/.container-fluid -->

      </nav>
</template>

<script>
import AuthBar from './Auth/AuthBar.vue';


export default {
    name: 'Navbar',
    components:{
      AuthBar,
    }
  }
</script>


<style scoped>
.navbar-main {
  overflow: hidden;
}

</style>
