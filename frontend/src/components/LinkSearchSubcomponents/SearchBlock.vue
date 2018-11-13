<template>
    <form class = "form-edit">
        <span>
        <input name="search" type="text" placeholder="Введите поисковый запрос" value="" id="input-search" class = "form-control" required autofocus>
        <button class="btn btn-lg btn-primary btn-block" type="button" id="search-start-button" v-on:click="SearchButtonClick()">Поиск</button>
        </span>
    <!-- <p>{{tmp}}</p> -->
    </form>
</template>
<script>
import Search from '../../SearchAlgorithms/search.js'


export default {
  name: 'SearchBlock',
  data: function ()
  {
     return {
        url : "api/search/number_of_links",
        searchResultsRaw: "[\
            {\"doc_id_from\": \"КСРФ/34-П/2018\",\"doc_id_to\": \"КСРФ/5-П/2007\",\"to_doc_title\": \"титл\",\"citations_number\": 1,\"contexts_list\": [\"Контектс\"],\"positions_list\": [9113]},\
            {\"doc_id_from\": \"КСРФ/34-П/2018\",\"doc_id_to\": \"КСРФ/5-П/2007\",\"to_doc_title\": \"титл\",\"citations_number\": 1,\"contexts_list\": [\"Контектс\"],\"positions_list\": [9113]}\
        ]",
        tmp:"none"
     } 
  },
  methods:{
      SearchButtonClick: function () {
        
        
        var searchRequst = document.getElementById('input-search').value;
        var requests = Search(searchRequst);
        if (requests == null)
        {
            this.$emit('SearchResultsReceived', null)
            return    
        }
        var rets = [];
        var counter = 0;
        var vue = this;        
        for (var req in requests)
        {
            var jsonReq = JSON.stringify(req);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', this.url, true);
            xhr.setRequestHeader("content-type", "application/json")
            
            xhr.withCredentials = true;
            xhr.send(jsonReq)

            xhr.onreadystatechange = function () {
                if (this.readyState != 4) return;
                if (this.status != 200) {
                    //console.log( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
                    counter += 1;
                    return;
                }
                var json = xhr.responseText
                var linkCount = JSON.parse(json)
                rets.push({Size: linkCount.size, IdFrom: req.idFrom, IdTo: req.idTo})
                counter += 1; 
            }

        }

        var waiter = function(){
            if (counter === requests.length)
                vue.$emit('SearchResultsReceived', rets);
            else
                setTimeout(waiter, 500);
        }
        setTimeout(waiter, 500);                



        // var idFrom = document.getElementById("input-uid-from").value
        // var idTo = document.getElementById("input-uid-to").value
        //     if (idFrom == 'any' || idFrom == '')
        //     idFrom = -1
        // if (idTo == 'any' || idTo == '')
        //     idTo = -1
        // if (idTo == idFrom)
        // {
        //     this.$emit('SearchResultsReceived', null)
        //     return    
        // }
        
        // var req = {doc_id_from:idFrom,doc_id_to:idTo}
        // var jsonReq = JSON.stringify(req)
        // var xhr = new XMLHttpRequest()
        // xhr.open('POST', this.url, true)
        // xhr.setRequestHeader("content-type", "application/json")
        
        // xhr.withCredentials = true;
        // var vue = this;        
        // xhr.send(jsonReq)

        // xhr.onreadystatechange = function () {
        //     if (this.readyState != 4) return;
        //     if (this.status != 200) {
        //         alert( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
        //         return;
        //     }
        //     var json = xhr.responseText
        //     //var json = this.searchResultsRaw
        //     var linkCount = JSON.parse(json)
        //     vue.tmp = linkCount
        //     var ret = {Size: linkCount.size, IdFrom: idFrom, IdTo: idTo}
        //     vue.$emit('SearchResultsReceived', ret)            
        // }
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
