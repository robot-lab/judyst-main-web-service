<template>
<div class="container">    
    <div class="search-result-block">
    <span class="page-list"><PageList v-bind:Count="LinksCount" v-bind:Step="Step" v-bind:Current="CurrentRange" v-on:PageChanged="getLinks($event)" /></span>
    <div class="links-block" v-if="isLoaded">
        <div v-for="Link in Links" :key="Link.id">
            <SearchResult v-bind:CleanLink="Link.Link" />
        </div>
    </div>
    <p v-else>Загружается...</p>
    </div>
</div>
</template>


<script>
import SearchResult from "./SearchResult.vue"
import PageList from "../PageList.vue"

 export default {
    name: 'SearchResultBlock',
    props: {
        LinksCount: Number,
        IdFrom: String,
        IdTo: String
    },
    data: function() {
        return {
            Step: 20,
            CurrentRange: [1, this.Step],
            url : '/api/search/get',
            tmp: null,
            Links: [],
            isLoaded : false
        }
    },
   
    components: {
        SearchResult,
        PageList
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
        var idFrom = this.IdFrom;
        var idTo = this.IdTo;
        if (idFrom == 'any')
            idFrom = -1
        if (idTo == 'any')
            idTo = -1
        if (idTo == idFrom)
        {
            return []    
        }
        
        var req = {doc_id_from:idFrom,doc_id_to:idTo, range:this.CurrentRange}
        var jsonReq = JSON.stringify(req)
        var xhr = new XMLHttpRequest()
        xhr.open('POST', this.url, true)
        xhr.setRequestHeader("content-type", "application/json")
        
        xhr.withCredentials = true;
        var vue = this ;       
        xhr.send(jsonReq)

        xhr.onreadystatechange = function(){
            if (this.readyState != 4) return;
            if (this.status != 200) {
                alert( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
                return;
            }
            var json = xhr.responseText
            vue.tmp = json
            var linkList = JSON.parse(json)
            var ret = []
            linkList = vue.fillContexts(linkList)
            for (var i = 0; i < linkList.length; i ++)
                ret.push({id: i, Link: linkList[i]})
            vue.Links = ret

            vue.isLoaded = true
        }
      }
    },

    created: function () {
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
  position: fixed;
  background-color: #EBEBEB
}
.page-list{
    position: relative;
    overflow: hidden;
}
.links-block{
    overflow: scroll;
}
</style>