<template>
<div class="container">    
    <!-- <p>{{tmp}}</p> -->
    <div class="search-result-block" v-if="LinksCount > 0">
        <p>Найдено: {{LinksCount}}</p>
        <span class="page-list">
            <PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" />
        </span>
       <div class="links-block" v-if="isLoaded">
            <LinkBoxView :Links="Links"/>
            <span class="page-list"><PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" /></span>
        </div> 
        <p v-else>Загружается...</p>
        
    </div>
    <div class="container" v-else>
            Поиск не дал результатов. 
    </div>
</div>
</template>


<script>
import SearchResult from "./SearchResult.vue"
import PageList from "../PageList.vue"
import LinkBoxView from "../views/LinksBoxView.vue"
import requsts from '../../utils/requests.js'
import urls from '../../utils/urls.js'

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

    computed: {
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
        LinkBoxView
    },

    methods: {
        
        getLinks: function (range)
      {
           
        this.CurrentRange = range;
        this.isLoaded = false;
        var vue = this;
        requsts.RequestLinks(range, this.url, this.SearchResults, function(links){
            vue.isLoaded = true; 
            vue.Links = links;
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

