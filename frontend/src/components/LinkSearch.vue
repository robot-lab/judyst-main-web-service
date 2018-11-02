<template>
  <div class="link-search-main">
      <SearchBlock class="search-block"  v-on:SearchResultsReceived="SearchResult=$event"/>
      <SearchResultsBlock v-if="SearchResult != null"
                          v-bind:LinksCount="SearchResult.Size"
                          v-bind:IdFrom="SearchResult.IdFrom" 
                          v-bind:IdTo="SearchResult.IdTo" />
  </div>
</template>

<script>
import SearchBlock from "./LinkSearchSubcomponents/SearchBlock.vue"
import SearchResultsBlock from "./LinkSearchSubcomponents/SearchResultsBlock.vue"
export default {
  name: 'LinkSearch',
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
