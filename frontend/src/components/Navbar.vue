<template>
<nav class="navbar fixed-top navbar-dark bg-dark  navbar-main">
        <div class="container-fluid">
          <div class="navbar-header">
            <router-link :to="'/'" class="navbar-brand" href="#">Judyst</router-link>
          </div>
        
        </div><!--/.container-fluid -->
      </nav>
</template>

<script>
  export default {
    name: 'Navbar',
  }
</script>


<style scoped>
.navbar-main {
  overflow: hidden;
}

</style>
