<template>
  <b-container class="link-search-main">
      <!-- <p>{{SearchRequest}} !! {{tmp}} @@ {{$route.params.request}}</p> -->
      <SearchBlock class="search-block"  :Request="SearchRequest" v-on:SearchResultsReceived="SearchResult=$event"/>
      <SearchResultsBlock v-if="SearchResult != null"
                          :SearchResults="SearchResult"/>

  </b-container>
</template>

<script>
import SearchBlock from "./SearchBlock.vue"
import SearchResultsBlock from "./SearchResultsBlock.vue"
export default {
  name: 'Search',
  data: function() {
      return {
        SearchResult: null,
        tmp : 'none',
        SearchRequest: null,

      }
  },
  methods:{
    SetSearchRequest: function(val)
    {
      if (val != undefined || val != null)
        this.SearchRequest = val.trim(); 
      else
        this.SearchRequest = ""; 
    }
  },
  created: function () {
    this.tmp = '1';
    this.SetSearchRequest(this.$route.params.request);
  },
  beforeRouteUpdate: function (to, from, next) {
    this.tmp = '2';
    this.SetSearchRequest(to.params.request); 
    next();
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
