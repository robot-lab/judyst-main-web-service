<template>
<b-container>
    <!-- <p>{{tmp}}</p> -->
       
    <div class="search-result-block" v-if="LinksCount > 0">
        <span class="page-list">
                <PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" />
        </span>
        <SearchStatistics  :SearchResults="SearchResults" :Count="LinksCount"/>
        <div class="links-block" v-if="isLoaded">
            <LinkBoxView :Links="Links" :DefaultCollapse="false"/>
            <span class="page-list"><PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" /></span>
        </div> 
        <p v-else>Загружается...</p>
    </div>
    <div class="container" v-else>
            Поиск не дал результатов. 
    </div>
</b-container>
</template>


<script>
import SearchResult from "./SearchResult.vue"
import SearchStatistics from "./SearchStatistics.vue"
import PageList from "../PageList.vue"
import LinkBoxView from "../views/LinksBoxView.vue"
import requsts from '../../utils/requests.js'
import urls from '../../utils/urls.js'
import StoreConst from '../../utils/searchHistoryConsts.js'

 export default {
    name: 'SearchResultBlock',
    props: {
        SearchResults: Array,
        
        
    },
    data: function() {
        return {
            Step: 10,
            CurrentRange: [1, 20],
            url : urls.Links,
            tmp: null,
            Links: [],
            isLoaded : false
        }
    },
    computed:{
        LinksCount: function () {
            var acum = 0;
            for (var i = 0; i < this.SearchResults.length; i++)
            {
                acum += this.SearchResults[i].Size;
            }
            return acum; 
        },
    },
    components: {
        SearchResult,
        PageList,
        LinkBoxView,
        SearchStatistics
    },

    methods: {
        
        getLinks: function (range)
      {
           
        this.CurrentRange = range;
        const req = JSON.stringify(this.SearchResults) + JSON.stringify(range);
        const storedRes = this.$store.getters.getStoredLinks(req) ;
        if (storedRes != null)
        {
            this.isLoaded = true; 
            this.Links = storedRes;
            return;
        }
        
        this.isLoaded = false;
        var vue = this;
        requsts.RequestLinks(range, this.url, this.SearchResults, function(links){
            vue.isLoaded = true; 
            vue.Links = links;
            vue.$store.commit(StoreConst.NEW_LINKS_PACK, {request: req, result: links});
        });

      },

      Initialize: function () {
        // this.tmp = this.LinksCount;
        this.CurrentRange = [1, this.Step];
        if (this.LinksCount < this.Step)
            this.CurrentRange[1] = this.LinksCount
        this.getLinks(this.CurrentRange)
          
      }
    },
    
    watch:{
        SearchResults: function () {
            this.Initialize();
            
        }
    },

    created: function () {
      this.Initialize();
    }
    
 }
    
</script>
<style scoped>
.search-result-block{
  overflow: auto;
  left: 15%;
  width:70%;
  height: 58%;
  position: relative;
}
.page-list{
    position: relative;
    overflow: hidden;
}


</style>

