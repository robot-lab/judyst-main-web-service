<template>
<b-container>
	<b-row>
        <div class="col-12">
            <div id="custom-search-input">
                <!-- @@@{{tmp}} -->
                <p v-if="isLoading"> Ведется поиск...</p>
                <div class="input-group">
                    <input type="text" id="input-search" class="search-query form-control" placeholder="Поиск"  :value="SearchRequest" @keyup.enter="SearchButtonClick()"/>
                    <span class="input-group-btn">
                        <button type="button"  >
                            <span class="fa fa-search" v-on:click="SearchButtonClick()"></span>
                        </button>
                    </span>
                </div>
            </div>
        </div>
	</b-row>
</b-container>
</template>



<script>
import requests from '../../utils/requests.js'
import urls from '../../utils/urls.js'
import router_urls from '../../utils/router_url.js'
import utils from '../../utils/common.js'
export default {
  name: 'SearchBlock',
  props:{
      Request: String,
  },
  data: function ()
  {
     return {
        url : urls.Search,
        SearchRequest: '',
        isLoading: false,
        tmp: "none"
     } 
  },
  methods:{
      SearchButtonClick: function () {
        
        var searchRequst = document.getElementById('input-search').value;
        searchRequst = utils.StashRequest(searchRequst);
        // this.tmp = searchRequst;
        this.$router.push(`${router_urls.Search}/${searchRequst}`);
        
       
        }
  },
 
  created: function () {
      if (this.Request != null)
      {
        this.SearchRequest = utils.DeStashRequest( this.Request);
        
        var vue = this;
        this.isLoading = true;
        requests.RequestSearch(this.SearchRequest, this.url, function(result){
            vue.$emit('SearchResultsReceived', result);
            vue.isLoading = false;
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
