<template>
    <form class = "form-edit">
        <input name="Document-from" type="text" placeholder="###-Type/Year" value="any" id="input-uid-from" class = "form-control" required autofocus>
        <input name="Document-to" type="text" placeholder="###-Type/Year" value="any" id="input-uid-to" class = "form-control" required >
        <button class="btn btn-lg btn-primary btn-block" type="button" id="search-start-button" v-on:click="SearchButtonClick()">Поиск</button>
    <p>{{tmp}}</p>
    </form>
</template>
<script>
export default {
  name: 'SearchBlock',
  data: function ()
  {
     return {
        url : "http://127.0.0.1:8000/api/search/get",
        searchResultsRaw: "[\
            {\"doc_id_from\": \"КСРФ/34-П/2018\",\"doc_id_to\": \"КСРФ/5-П/2007\",\"to_doc_title\": \"титл\",\"citations_number\": 1,\"contexts_list\": [\"Контектс\"],\"positions_list\": [9113]},\
            {\"doc_id_from\": \"КСРФ/34-П/2018\",\"doc_id_to\": \"КСРФ/5-П/2007\",\"to_doc_title\": \"титл\",\"citations_number\": 1,\"contexts_list\": [\"Контектс\"],\"positions_list\": [9113]}\
        ]",
        tmp:"none"
     } 
  },
  methods:{
      SearchButtonClick: function () {
        var idFrom = document.getElementById("input-uid-from").value
        var idTo = document.getElementById("input-uid-to").value
        if (idFrom == 'any')
            idFrom = -1
        if (idTo == 'any')
            idTo = -1
        if (idTo == idFrom)
        {
            this.$emit('SearchResultsReceived', null)
            return    
        }
        
        var req = {doc_id_from:idFrom,doc_id_to:idTo}
        var jsonReq = JSON.stringify(req)
        var xhr = new XMLHttpRequest()
        xhr.open('POST', this.url, false)
        xhr.setRequestHeader("content-type", "application/json")
        xhr.setRequestHeader("Access-Control-Allow-Origin", "*")
        
        xhr.withCredentials = true;
        
        xhr.send(jsonReq)
        var json = xhr.responseText
        //var json = this.searchResultsRaw
        var linkList = JSON.parse(json)
        this.tmp = linkList.length
        var ret = []
        for (var i = 0; i < linkList.length; i ++)
            ret.push({id: i, Link: linkList[i]})
        this.$emit('SearchResultsReceived', ret)
        return
    
      }
  }
}
</script>
 

 <style scoped>
 
    .form-edit {
    width: 100%;
    max-width: 330px;
    padding: 15px;
    margin: 0 auto;
    }
    .form-edit .checkbox {
    font-weight: 400;
    }
    .form-edit .form-control {
    position: relative;
    box-sizing: border-box;
    height: auto;
    padding: 10px;
    font-size: 16px;
    }
    .form-edit .form-control:focus {
    z-index: 2;
    }
    .form-edit input[type="email"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
    }
    .form-edit input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    }

 </style>
