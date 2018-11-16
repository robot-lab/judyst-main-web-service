<template>
<div class="container">    
    <!-- <p>{{tmp}}</p> -->
    <div class="search-result-block" v-if="LinksCount > 0">
        <span class="page-list"><PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" /></span>
        <div class="links-block" v-if="isLoaded">
            <div v-for="Link in Links" :key="Link.id">
                <SearchResult v-bind:CleanLink="Link.Link" />
            </div>
        <span class="page-list"><PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" /></span>
        <FooterController/>
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
import FooterController from "../FooterController.vue"

 export default {
    name: 'SearchResultBlock',
    props: {
        SearchResults: Array,
        
    },
    data: function() {
        return {
            Step: 10,
            CurrentRange: [1, 20],
            url : 'api/search/get',
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
        FooterController
    },

    methods: {
        fillContexts: function(links)
        {
            for (var i = 0; i < links.length; i++)
            {
                var link = links[i];
                link.contexts = []
                for(var j = 0; j < link.positions_list.length; j++)
                {
                    var position = link.positions_list[j]
                    var before = link.text.substr(position.context_start,
                                                    position.link_start - position.context_start)
                    var citation = link.text.substr(position.link_start,
                                                    position.link_end - position.link_start)
                    var after = link.text.substr(position.link_end,
                                                    position.context_end - position.link_end)
                    
                    var context = {before: before, citation: citation, after: after}
                    // this.tmp = link.positions_list[j]
                    link.contexts.push(context)

                }
                links[i] = link
            }
            return links
        },

        getLinks: function (range)
      {
           
        this.CurrentRange = range;
        this.isLoaded = false;
        
        var peakedLinksCount = 0; 
        var i = 0;
        var startedCoutnter = 0; 
        var finishedCounter = 0; 
        var vue = this ;       
        var url = this.url;
        var links = []
        
        var get = function (range, searchResult) {
            
            var req = {doc_id_from: searchResult.doc_id_from,
                       doc_id_to: searchResult.doc_id_to,
                       range: range}
            var jsonReq = JSON.stringify(req);
            // vue.tmp = searchResult;
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader("content-type", "application/json");
            
            xhr.send(jsonReq);

            xhr.onreadystatechange = function(){
                if (this.readyState != 4) return;
                if (this.status != 200) {
                    alert( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
                    return;
                }
                var json = xhr.responseText
                var linkList = JSON.parse(json)
                var ret = []
                linkList = vue.fillContexts(linkList)
                for (var i = 0; i < linkList.length; i ++)
                    ret.push({id: i, Link: linkList[i]})
                links = links.concat(ret)
                finishedCounter++;
                // vue.tmp = {a: startedCoutnter, b: finishedCounter};
            }
        }
        // vue.tmp = this.SearchResults;
        // vue.tmp = i; 
        while (i < this.SearchResults.length && peakedLinksCount < range[0])
        {
            if (peakedLinksCount + this.SearchResults[i].Size <= range[0])
            {
                // vue.tmp = {a:peakedLinksCount + this.SearchResults[i].Size, b:range[0]};
                peakedLinksCount += this.SearchResults[i].Size;
                i++;
            }
            else
            {
                var min_point = range[0] - peakedLinksCount;
                if (peakedLinksCount + this.SearchResults[i].Size <= range[1])
                {
                    var currRange = [min_point, this.SearchResults[i].Size]
                    peakedLinksCount += this.SearchResults[i].Size; 
                }
                else
                {
                    var max_point =  range[1] - peakedLinksCount ;
                    currRange = [min_point, max_point ]; 
                    peakedLinksCount += range[1] - range[0]; 
                }
                startedCoutnter++;
                var j = i; 
                setTimeout(function(){
                    // vue.tmp = i; 
                    
                    get(currRange, vue.SearchResults[j]);},0);
                i++;
                break;
            }

        }
        while (i < this.SearchResults.length && peakedLinksCount < range[1])
        {
            if (peakedLinksCount + this.SearchResults[i].Size <= range[1])
            {
                
                currRange = [0, this.SearchResults[i].Size];
                peakedLinksCount += this.SearchResults[i].Size;
                
            }
            else
            {
                currRange = [0, range[1] - peakedLinksCount]
                peakedLinksCount = range[1]
            }
            j = i;
            setTimeout(function(){get(currRange, vue.SearchResults[j]);},0);
            startedCoutnter++;
            i++;
        }
        var checker = function(){
            // vue.tmp = {a: startedCoutnter, b: finishedCounter};
            if (startedCoutnter <= finishedCounter)
            {

                vue.Links = links;
                vue.isLoaded = true;
            }
            else
            setTimeout(checker, 500);
        };
        setTimeout(checker, 0);
        

      }
    },

    created: function () {
        // this.tmp = this.LinksCount;
        this.CurrentRange = [1, this.Step];
        if (this.LinksCount < this.Step)
            this.CurrentRange[1] = this.LinksCount
        this.getLinks(this.CurrentRange)
    }
    
 }
    
</script>
<style scoped>
.search-result-block{
  overflow: auto;
  top: 35%;
  left: 15%;
  width:70%;
  height: 58%;
  position: relative;
}
.page-list{
    position: relative;
    overflow: hidden;
}
.links-block{
}

</style>

