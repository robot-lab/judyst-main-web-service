<template>
<div class="container">
	<div class="row">
        <div class="col-12">
            <div id="custom-search-input">
                <div class="input-group">
                    <input type="text" id="input-search" class="search-query form-control" placeholder="Поиск" />
                    <span class="input-group-btn">
                        <button type="button"  >
                            <span class="fa fa-search"  v-on:click="SearchButtonClick()"></span>
                        </button>
                    </span>
                </div>
            </div>
        </div>
	</div>
</div>
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
        for (var i = 0; i < requests.length; i++)
        {
            var req = requests[i];
            // this.tmp = req;

            var jsonReq = JSON.stringify(req);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', this.url, true);
            xhr.setRequestHeader("content-type", "application/json")
            
            xhr.send(jsonReq)
            vue.tmp = []
            xhr.onreadystatechange = function () {
                if (this.readyState != 4) return;
                if (this.status != 200) {
                    //console.log( 'ошибка: ' + (this.status ? this.statusText : 'запрос не удался') );
                    counter += 1;
                    return;
                }
                var json = this.responseText + '';
                vue.tmp.push(req);
                var linkCount = JSON.parse(json)
                rets.push({Size: linkCount.size, doc_id_from: req.doc_id_from, doc_id_to: req.doc_id_to})
                counter += 1; 
            }

        }

        var waiter = function(){
            if (counter === requests.length)
                {
                    vue.$emit('SearchResultsReceived', rets);
                    // vue.tmp = rets;    
                }
            else
                setTimeout(waiter, 500);
        }
        setTimeout(waiter, 500);                


      }
  }
}
</script>
 

 <style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css');

.container{
    padding: 10%;
    text-align: center;
}
#custom-search-input {
    margin:0;
    margin-top: 10px;
    padding: 0;
}
 
#custom-search-input .search-query {
    width:100%;
    padding-right: 3px;
    padding-left: 15px;
        /* IE7-8 doesn't have border-radius, so don't indent the padding */
    margin-bottom: 0;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 0;
}
 
#custom-search-input button {
    border: 0;
    background: none;
    /** belows styles are working good */
    padding: 2px 5px;
    margin-top: 2px;
    position: absolute;
    right:0;
    /* IE7-8 doesn't have border-radius, so don't indent the padding */
    margin-bottom: 0;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    border-radius: 3px;
    color:#D9230F;
    cursor: unset;
    z-index: 2;
}
 
.search-query:focus{
    z-index: 0;   
}

 </style>
