<template>
<b-container fluid class="wrap">
    <div v-if="CurrentDocument != null">
        <!-- <p>{{tmp}}</p> -->
        <h5 class="title-block"><b>Заголовок документа:</b> <p>{{CurrentDocument.title}}</p></h5>
        <h4 class="id-block"> <p><b>Номер документа:</b> {{CurrentDocument.doc_id}}</p></h4>
        <h4 class="date-block"><p><b>Дата публикации:</b> {{CurrentDocument.release_date}} </p></h4>
        <b-card>
            <b-container v-if="LinksTo!= null">
            <b-card-header v-b-toggle="'link_to_block'">Цитирование этого документа</b-card-header>
            <b-collapse id="link_to_block"><b-card-body >
                <multipage-links-view :SearchResults="LinksTo" :Step="5" :DefaultCollapse="true"/>
            </b-card-body></b-collapse>
            </b-container>
            <p v-else> Выполняется предобработка...</p>
        </b-card>
        <div class="text-block" >
            
            <!-- {{LinksTo}} -->
            <!-- {{SortedAloneLinks}} -->
            <div v-if="ProcessedText !== null">
                <v-runtime-template :template="ProcessedText"/>
            </div>
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
import VRuntimeTemplate from "v-runtime-template";
import multipageLinksView from './MultipageLinksView.vue'
import requests from '../../utils/requests.js'
import utils from '../../utils/common.js'
import urls from '../../consts/urls.js'
// import marks from '../../SearchAlgorithms/marks.js'
export default {
    name: 'DocumentView',
    components:{
        multipageLinksView,
        VRuntimeTemplate

    },
    data: function(){
        return {
            Step: 5,
            LinksTo: null,
            LinksPackFrom: null,
            CurrentDocument: null,
            tmp: 'none',

        }
    },
    computed:{
        SortedAloneLinks: function () {
            if (this.LinksPackFrom === null || this.LinksTo === null)
                return null;
            var links = [];
            for (var i = 0; i < this.LinksPackFrom.length; i++)
            {
                var linkObj = this.LinksPackFrom[i];
                for(var j = 0; j < linkObj.positions_list.length; j++)
                    var linkAlone = {
                        doc_id_from : linkObj.doc_id_from,
                        doc_id_to : linkObj.doc_id_to,
                        to_doc_title: linkObj.to_doc_title,
                        position: linkObj.positions_list[j]
                    }
                links.push(linkAlone);
            }
            

            links.sort(function(linkA,linkB){
                return linkA.position.link_start - linkB.position.link_end;
            });
            return links;
            
        },
        ProcessedText: function(){
            if (this.CurrentDocument === null || this.SortedAloneLinks === null)
                return null;
            var allText = this.CurrentDocument.text;
            var text = '<div><template>';
            var last = 0;
           for (var i = 0; i < this.SortedAloneLinks.length; i++)
           {
               var linkAlone = this.SortedAloneLinks[i];
               text += allText.slice(last, linkAlone.position.link_start);
               var linkText = allText.slice(linkAlone.position.link_start, linkAlone.position.link_end +1);
            //    this.tmp = linkText;
               text += `<b-btn size="sm" variant="link"  @click="OpenLink('/document/${utils.StashDocId(linkAlone.doc_id_to)}/0')">${linkText}</b-btn>`;
               last = linkAlone.position.link_end;
           }
            text += allText.slice(last, allText.length); 
            text += '</template></div>'
            return text;
        },
    },
    methods:{
        OpenLink: function (path)
        {
            this.$router.push(path);
            this.tmp = path;
        },
        Init: function(route)
        {

            this.LinksTo = null;
            this.LinksPackFrom = null;
            this.CurrentDocument = null;
            var doc_id = utils.DeStashDocId(route.params.doc_id);
            var vue = this;
           
            requests.RequestDocument(doc_id, urls.Document, function(doc, error){
                if (doc === null)
                    {
                        alert('Error while getting document. Error code: ' + error)

                    }
                vue.CurrentDocument = doc; 
                
            });

            requests.RequestSearch(`*->${doc_id}`, urls.Search, function (result){
                    vue.LinksTo = result;
                });
            
            requests.RequestSearch(`${doc_id}->*`, urls.Search, function (result){
                requests.RequestLinks([1, result.Size], urls.Links, result, function (links) {
                    vue.LinksPackFrom = links; 
                    // vue.tmp += 'from ready(' + links + ');' ; 
                    
                });
                
            });
        }
    },


    created:function () {
        this.Init(this.$route);

    },
    beforeRouteUpdate: function(to, from, next){
        this.Init(to);
        next();
    }
  
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
    margin-top: 5%;
    line-height: 1.5;
    text-align: left;
}
.link{
    z-index: 2;
}
</style>

