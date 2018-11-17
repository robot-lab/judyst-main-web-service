<template>
<div class="container">
	<div class="row">
        <div class="col-12">
            <div id="custom-search-input">
                <div class="input-group">
                    <input type="text" id="input-search" class="search-query form-control" placeholder="Поиск" @keyup.enter="SearchButtonClick()"/>
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
import requests from '../../utils/requests.js'
import urls from '../../utils/urls.js'


export default {
  name: 'SearchBlock',
  data: function ()
  {
     return {
        url : urls.Search,
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
        var vue = this;
        requests.RequestSearch(searchRequst, this.url, function(result){
            vue.$emit('SearchResultsReceived', result);
        });
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
