<template>
<b-container fluid class="wrap">
    <div v-if="CurrentDocument != null">
        <!-- <p>{{tmp}}</p> -->
        <h5 class="title-block"><b>Заголовок документа:</b> <p>{{CurrentDocument.title}}</p></h5>
        <h4 class="id-block"> <p><b>Номер документа:</b> {{CurrentDocument.doc_id}}</p></h4>
        <h4 class="date-block"><p><b>Дата публикации:</b> {{CurrentDocument.release_date}} </p></h4>
        <div class="text-block" >
            
            <!-- {{LinksPackFrom}} -->
            <!-- {{SortedAloneLinks}} -->
            <p v-if="ProcessedText != null" v-html="ProcessedText">
            </p>
            <p v-else>
                Выполняется предобработка...
            </p>
        </div>
    </div>
    <div v-else>
        <p>Документ загружается...</p>
    </div>
</b-container>
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

        SortedAloneLinks: function () {
            if (this.LinksPackFrom === null || this.LinksPackTo === null)
                return null;
            var links = [];
            for (var i = 0; i < this.LinksPackFrom.length; i++)
            {
                var linkObj = this.LinksPackFrom[i];
                for(var j = 0; j < linkObj.Link.positions_list.length; j++)
                    var linkAlone = {
                        doc_id_from : linkObj.Link.doc_id_from,
                        doc_id_to : linkObj.Link.doc_id_to,
                        to_doc_title: linkObj.Link.to_doc_title,
                        position: linkObj.Link.positions_list[j]
                    }
                links.push(linkAlone);
            }
            for (i = 0; i < this.LinksPackTo.length; i++)
            {
                linkObj = this.LinksPackTo[i];
                    for(j = 0; j < linkObj.Link.positions_list.length; j++)
                        linkAlone = {
                            doc_id_from : linkObj.Link.doc_id_from,
                            doc_id_to : linkObj.Link.doc_id_to,
                            to_doc_title: linkObj.Link.to_doc_title,
                            position: linkObj.Link.positions_list[j]
                    }
                links.push(linkAlone);
            }

            links.sort(function(linkA,linkB){
                return linkA.position.link_start - linkB.position.link_end;
            });
            return links;
            
        },
        ProcessedText: function(){
            if (this.CurrentDocument === null || this.LinksPackFrom === null || this.LinksPackTo === null)
                return null;
            var allText = this.CurrentDocument.text;
            var text = '';
            // '<router-link :to="`/document/${utils.StashDocId(CleanLink.doc_id_from)}/0`">{{CleanLink.doc_id_from}}</router-link>'
            var last = 0;
           for (var i = 0; i < this.SortedAloneLinks.length; i++)
           {
               var linkAlone = this.SortedAloneLinks[i];
               text += allText.slice(last, linkAlone.position.link_start);
               var linkText = allText.slice(linkAlone.position.link_start, linkAlone.position.link_end +1);
            //    this.tmp = linkText;
               text += `<span class="link" href="#" @click="OpenLink(\`/document/${utils.StashDocId(linkAlone.doc_id_from)}/0\`)">${linkText}</span>`;
               last = linkAlone.position.link_end;
           }
            text += allText.slice(last, allText.length); 
            return text;
        },
    },
    methods:{
        OpenLink: function (path)
        {
            this.$router.push(path);
        }
    },


    created:function () {


        var doc_id = utils.DeStashDocId(this.$route.params.doc_id);
        var vue = this;
        // var req = `${doc_id}->${marks.any_front}`;
        // requests.RequestSearch(req, urls.Search, function(SearchResult){
        //     searchResults = {}
        // });
        requests.RequestDocument(doc_id, urls.Document, function(doc, error){
            if (doc === null)
                {
                    alert('Error while getting document. Error code: ' + error)

                }
            vue.CurrentDocument = doc; 
            
        });

        requests.RequestSearch(`*->${doc_id}`, urls.Search, function (result){
            requests.RequestLinks([1, result.Size], urls.Links, result, function (links) {
                vue.LinksPackTo = links; 
                // vue.tmp += 'to ready(' + links + ');'; 
                
            }); });
        
        requests.RequestSearch(`${doc_id}->*`, urls.Search, function (result){
            requests.RequestLinks([1, result.Size], urls.Links, result, function (links) {
                vue.LinksPackFrom = links; 
                // vue.tmp += 'from ready(' + links + ');' ; 
                
            });
            
        });
    },

}
</script>



<style scoped>
.wrap{
    position: relative;
    padding-top: 3%; 
}

.title-block{
padding: 3%;
}
.id-block{
text-align: left;
}
.date-block{
text-align: left;
}
.text-block{
    position: relative;
    margin-top: 1%;
    text-align: justify;
}
.link{
    background-color: #555555;
    color: blue;
}
</style>

