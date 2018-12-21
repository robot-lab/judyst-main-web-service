<template>
<b-container >
    <!-- <p>{{tmp}}</p> -->
    <div class="search-result-block" v-if="LinksCount > 0">
        <span class="page-list">
            <PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" />
        </span>
       <div class="links-block" v-if="isLoaded">
            <b-card-group>
                <LinkBoxView :Links="Links" :CollapseDefault="CollapseDefault"/>
            </b-card-group>
            <span class="page-list"><PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" /></span>
       </div> 
        <p v-else>Загружается...</p>
        
    </div>
    <b-container v-else>
            Не обнаружено.
    </b-container>

</b-container>
</template>


<script>
import PageList from "../PageList.vue"
import LinkBoxView from "./LinksBoxView.vue"
import requsts from '../../utils/requests.js'
import url from '../../consts/urls.js'
import StoreConst from '../../consts/store_consts.js'

 export default {
    name: 'MultipageLinksView',
    props: {
        SearchResults: Array,
        Step: Number, 
        CollapseDefault: Boolean

        
    },
    data: function() {
        return {
            CurrentRange: [1, this.Step],
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
        StoredLinks: function () {
            
            return this.$store.StoredLinks; 
        }



    },
   
    components: {
        PageList,
        LinkBoxView
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
        requsts.RequestLinks(range, url.Links, this.SearchResults, function(links){
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

