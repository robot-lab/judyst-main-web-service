<template>
  <b-container class="link-search-main">
      <!-- <p>{{SearchRequest}} !! {{tmp}} @@ {{$route.params.request}}</p> -->
      <!-- <p>{{tmp}}</p> -->
      <!-- <p>Result: {{StoredResult}}</p> -->
      <SearchBlock class="search-block"  :Request="SearchRequest" v-on:SearchResultsReceived="SetSearchResult($event)" :isNeedSearch="isNeedSearch"/>
      <SearchResultsBlock v-if="SearchResult != null"
                          :SearchResults="SearchResult"/>

  </b-container>
</template>

<script>
import SearchBlock from "./SearchBlock.vue"
import SearchResultsBlock from "./SearchResultsBlock.vue"
import StoreConsts from "../../utils/searchHistoryConsts.js"
export default {
  name: 'Search',
  data: function() {
      return {
        SearchResult: null,
        tmp : 'none',
        SearchRequest: null,
        isNeedSearch: true,
      }
  },
  computed: {
    StoredResult: function () {
      return this.$store.getters.storedResults;      
    }
  },
  methods:{
    SetSearchRequest: function(val)
    {
      val = val.trim();
      if (val != undefined || val != null)
        {
            if (this.$store.getters.getStoredRes(val) == null)
            {
              this.isNeedSearch = true;
            }
            else
            { 
              this.isNeedSearch = false; 
              this.SearchResult = this.$store.getters.getStoredRes(val);
            }
            this.SearchRequest = val;
        }
      else
        this.SearchRequest = ""; 
    },
    
    SetSearchResult: function(val)
    {
        this.tmp = ':)';
        this.$store.commit(StoreConsts.NEW_SEARCH_RESULT, {request: this.SearchRequest, result: val});
        this.SearchResult = val;
    }
  },
  created: function () {
    // this.tmp = '1';
    this.SetSearchRequest(this.$route.params.request);
  },
  beforeRouteUpdate: function (to, from, next) {
    // this.tmp = '2';
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
