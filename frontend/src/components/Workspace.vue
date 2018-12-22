<template>
<b-container class="workspace">
    <router-view/>
</b-container>
</template>


<script>
import StoreConst from '../consts/store_consts.js';
export default {
  name: 'Workspace',
  components: {
  },
  created: function (){

    this.$store.dispatch(StoreConst.UPDATE_FROM_STORAGE).then();
  }

  }
    
 

</script>


<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

</style>

