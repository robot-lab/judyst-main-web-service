<template>
    <b-container>
        <b-card md-8>
            <b-card-header v-b-toggle="`favorite-requests-collapse${isModal?'-modal':''}`">
               Избранные запросы
            </b-card-header>
            <b-collapse :id="`favorite-requests-collapse${isModal?'-modal':''}`"
                        :visible="!isModal" >
                <b-card-body class="content">
                    <b-container   v-if="!isRequestsEmpty">
                        <b-card class=" text-center content-card" 
                                v-for="(req, ind) in Requests" :key=ind>
                                <h5>{{req.caption}}</h5>
                                <h7><i>{{req.body}}</i></h7>
                                <span v-if="req.description != ''">
                                    <p> {{req.description}}</p>
                                </span>
                            <b-card-footer>
                                <b-row v-if="!isModal">
                                    <b-btn size="sm" class="control first-control" variant="link" :to="GetReqPath(req.body)">Применить</b-btn>
                                    <b-btn size="sm" class="control" variant="outline-success" @click="Edit('request', req.body, req)">Редактировать</b-btn>
                                    <b-btn size="sm" class="control" variant="danger" @click="DelReq(req.body)">Удалить</b-btn>
                                </b-row>
                                <b-btn v-else size="sm" class="control first-control" variant="link" :to="GetReqPath(req.body)">Invoke</b-btn>
                            </b-card-footer>
                            </b-card>
                    </b-container>
                    <div v-else>
                        Нет избранных запросов. 
                    </div>
                </b-card-body>
            </b-collapse>
            <b-card-footer v-if="!isModal">
                <b-btn  variant="success" size="sm" :to="newRequestUrl">Новый запрос </b-btn>
            </b-card-footer>
        </b-card>


         <b-card md-8>
            <b-card-header v-b-toggle="`favorite-documents-collapse${isModal?'-modal':''}`">
                Избранные документы
            </b-card-header>
              <b-collapse :id="`favorite-documents-collapse${isModal?'-modal':''}`"
                        :visible="!isModal" >
                <b-card-body class="content">
                    <b-container   v-if="!isDocumentsEmpty">
                        <b-card class=" text-center content-card" 
                                v-for="(req, ind) in Documents" :key=ind 
                                :title="req.caption"
                                :sub-title="req.body">
                            
                                <span v-if="req.description != ''">
                                    <p> {{req.description}}</p>
                                </span>
                                <span v-b-toggle="`doc-${req.body}-title-${ind}`">Заголовок</span>
                                <b-collapse :id="`doc-${req.body}-title-${ind}`" class="text-center">
                                    {{req.title}}
                                </b-collapse>
                            <b-card-footer>
                                <b-row v-if="!isModal">
                                    <b-btn size="sm" class="control first-control" variant="link" :to="GetDocPath(req.body)">Документ</b-btn>
                                    <b-btn size="sm" class="control" variant="outline-success" @click="Edit('document', req.body, req)">Редактировать</b-btn>
                                    <b-btn size="sm" class="control" variant="danger" @click="DelDoc(req.body)">Удалить</b-btn>
                                </b-row>
                                <hr>
                                <b-row>
                                    <b-btn size="sm" class="control first-control" variant="link" :to="GetReqLinks(req.body, 'from')">Ссылки из</b-btn>
                                    <b-btn size="sm" class="control" variant="link" :to="GetReqLinks(req.body, 'to')">Ссылки в</b-btn>
                                </b-row>
                                    
                            </b-card-footer>
                            </b-card>
                    </b-container>
                    <div v-else>
                        Нет избранных документов
                    </div>
                </b-card-body>
            </b-collapse>
            <!-- <b-card-footer>
                <b-btn v-if="!isModal" variant="success" size="sm" :to="newDocumentUrl">New document</b-btn>
            </b-card-footer> -->
        </b-card>

            
    </b-container>
</template>


<script>
import router_urls from '../../consts/router_url.js'
import StoreConsts from '../../consts/store_consts.js'
import utils from '../../utils/common.js'
import marks from '../../SearchAlgorithms/marks.js'
import delimiters from '../../SearchAlgorithms/delimiters.js'


export default {
    name: 'UserFavoritesView',
    props: {
        isModal: Boolean
    },
    data: ()=>{return {
        newRequestUrl: `${router_urls.AddFavorite}/request`,
        newDocumentUrl: `${router_urls.AddFavorite}/document`,
        fullView: router_urls.UserFavorites,
        salt : '',

    }},
    computed:{
       
        Requests: function(){
            if (this.salt != '')
                return {};
            return this.$store.getters.favoriteRequests; 
        },
        Documents: function(){
            if (this.salt != '')
                return {};
            return this.$store.getters.favoriteDocuments; 
        },
        isRequestsEmpty: function(){
            if (this.salt != '')
                return false; 
            return Object.keys(this.Requests).length == 0;
        },
          isDocumentsEmpty: function(){
            if (this.salt != '')
                return false; 
            return Object.keys(this.Documents).length == 0;
        },
    },
    methods:{
       
        GetReqPath: function (req) {
            return `${router_urls.Search}/${req}`;
        },
        GetReqLinks: function (doc_id, side) {
            let req = ''; 
            if (side == 'from')
                req = `${doc_id}${delimiters.CitationPartsDelimiter}${marks.any_front}`;
            else
                req = `${marks.any_front}${delimiters.CitationPartsDelimiter}${doc_id}`;

            return `${router_urls.Search}/${utils.StashRequest(req)}`;
        },
        GetDocPath: function (req) {
            return `document/${req}`;
        },
        DelReq: function(req){
            this.$store.commit(StoreConsts.DELETE_FAVORITE_REQ, req);
        },
        DelDoc: function(doc){
            this.$store.commit(StoreConsts.DELETE_FAVORITE_DOC, doc);
        },
        Edit: function (target, body) {
            let bd = '';
            if (target == 'request')
                bd = utils.StashRequest(body);
            else
                bd = utils.StashDocId(body);
            
            this.$router.push(`${router_urls.AddFavorite}/${target}/${bd}`);

        },
        GoToNew: function (where){
            this.$emit('finish');
            if (where == 'request')
                this.$router.push(this.newRequestUrl);
            else
                this.$router.push(this.newDocumentUrl);
        },
        created:function(){
            let vue = this;
            if (this.isModal)
                this.$store.commit(StoreConsts.SET_ON_FAVORITE_UPDATE, 
                    ()=>{
                        vue.salt = 'reinvoking';
                        vue.salt = ''; 
                    });
        },
        destroyed: function(){
            if (this.isModal)
                this.$store.commit(StoreConsts.DELETE_ON_FAVORITE_UPDATE);
        }



    },
   

}
</script>



<style scoped>
.content{
  position: relative;
  width: 100%;
}
.content-card{
  width: 100%;
  padding-left: 3%;
  padding-right: 3%;
  overflow: hidden;
  word-wrap: break-word; 
  margin-bottom: 5%;
}
.control{
    margin-right: 4%;
}
.first-control{
    margin-left: 15%;
}
</style>


