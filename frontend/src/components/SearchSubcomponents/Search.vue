<template>
  <div class="link-search-main container">
      <!-- <p>{{$route.params.request}}</p> -->
      <SearchBlock class="search-block"  :Request="$route.params.request" v-on:SearchResultsReceived="SearchResult=$event"/>
      <SearchResultsBlock v-if="SearchResult != null"
                          v-bind:SearchResults="SearchResult"/>

  </div>
</template>

<script>
import SearchBlock from "./SearchBlock.vue"
import SearchResultsBlock from "./SearchResultsBlock.vue"
export default {
  name: 'Search',
  data: function() {
      return {
    
        SearchResult: null,
        tmp : 'none'

      }
  },
  computed:{
   
  },
  
  methods:
  {
  },
  components:{
    SearchBlock,
    SearchResultsBlock
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.search-block{
  top:10%;

}
.link-search-main{
  overflow: hidden ;
}
</style>
