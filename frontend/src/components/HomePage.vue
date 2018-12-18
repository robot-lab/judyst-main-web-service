<template>
<div class="container ">
    <!-- <Search/> -->
    <b-container>
        <p>{{description}}</p>
        <!-- <p>Token: {{token}}</p> -->
    </b-container>
</div>
</template>


<script>
import Search from './SearchSubcomponents/Search'

const description = 'Tempor ut laborum ex excepteur laborum duis. Incididunt et nisi aliquip deserunt ea Lorem sit officia et consequat dolor ad adipisicing. Sint elit dolore esse consectetur dolore ut ullamco deserunt eiusmod sint. Non ut amet nisi non proident ex consequat commodo irure tempor in sit. Nostrud consectetur do labore eu amet exercitation velit aliqua nulla anim ipsum excepteur. Lorem amet magna adipisicing fugiat quis anim sit ipsum voluptate qui veniam velit in ex. Laboris pariatur commodo eiusmod velit cillum sint veniam amet.';

export default {
  name: 'HomePage',
  data : function () {
      return {
          description,

      }
  },
  components:{
      Search,
  },
  computed: {
      token : function () {
          return this.$store.token;
      }
  }
}
</script>


<style>

</style>

