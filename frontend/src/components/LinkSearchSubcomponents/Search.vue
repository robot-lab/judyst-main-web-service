<template>
  <div class="link-search-main">
      <SearchBlock class="search-block"  v-on:SearchResultsReceived="SearchResult=$event"/>
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
    
        SearchResult: null

      }
  },
  components:{
    SearchBlock,
    SearchResultsBlock
  },
  methods:
  {
  }
 
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.search-block{
  top:10%;

}
.link-search-main{
  overflow: auto;
}
</style>
