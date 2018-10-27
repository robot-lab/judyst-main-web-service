<template>
<div class="workspace container ">
    <router-view/>
</div>
</template>


<script>
import LinkSearch from './LinkSearch.vue';
export default {
  name: 'Workspace',
  components: {
      LinkSearch
  }
    
 
}
</script>


<style>

</style>

