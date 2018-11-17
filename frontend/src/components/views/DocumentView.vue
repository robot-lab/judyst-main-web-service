<template>
<div class="wrap container-fluid">
    <div v-if="CurrentDocument != null">
    <h5>{{CurrentDocument.title}}</h5>
        <div class="text-block" >
            {{ProcessedText}}
        </div>
    </div>
    <div v-else>
        <p>Документ загружается...</p>
    </div>
</div>
</template>

<script>
import LinksBoxView from './LinksBoxView.vue'

import requests from '../../utils/requests.js'
import utils from '../../utils/common.js'
import urls from '../../utils/urls.js'
// import marks from '../../SearchAlgorithms/marks.js'
export default {
    name: 'DocumentView',
    components:{
        LinksBoxView,
    },
    data: function(){
        return {
            Step: 5,
            LinksPackTo: null,
            LinksPackFrom: null,
            CurrentDocument: null,
            tmp: 'none',

        }
    },
    computed:{
        ProcessedText: function(){
            return this.CurrentDocument.text;
        },
        
    },



    created:function () {


        var doc_id = utils.DeStashDocId(this.$route.params.doc_id);
        var vue = this;
        // var req = `${doc_id}->${marks.any_front}`;
        // requests.RequestSearch(req, urls.Search, function(SearchResult){
        //     searchResults = {}
        // });
        requests.RequestDocument(doc_id, urls.Document, function(doc){
            vue.CurrentDocument = doc; 
            vue.tmp = doc;
        });


}
}
</script>



<style scoped>
.wrap{
    position: relative;
}

.text-block{
    position: relative;
    margin-top: 1%;
    text-align: justify;
}
</style>

