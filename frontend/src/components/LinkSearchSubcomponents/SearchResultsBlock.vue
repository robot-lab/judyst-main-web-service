<template>
<div class="container">    
    <PageList v-bind:Count="LinksCount" 
            v-bind:Step="this.Step"
            v-bind:Current="CurrentRange"
            v-on:PageChanged="CurrentRange = $event"/>
    <div class = "search-result-block">
        <div v-for="Link in Links" :key="Link.id">
            <SearchResult v-bind:CleanLink="Link.Link" />
        </div>
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
            url : '/api/search/get'
        }
    },
    computed:
    {
      Links: function ()
      {
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
        xhr.open('POST', this.url, false)
        xhr.setRequestHeader("content-type", "application/json")
        
        xhr.withCredentials = true;
        
        xhr.send(jsonReq)
        var json = xhr.responseText
        var linkList = JSON.parse(json)
        var ret = []
        for (var i = 0; i < linkList.length; i ++)
            ret.push({id: i, Link: linkList[i]})
        return ret
      }

    },
    components: {
        SearchResult,
        PageList
    },

    created: function () {
        if (this.LinksCount < this.Step)
            this.CurrentRange[1] = this.LinksCount
        
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
</style>