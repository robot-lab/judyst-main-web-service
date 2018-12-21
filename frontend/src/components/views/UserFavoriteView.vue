<template>
    <b-container>
        <p>Hello</p>
        <b-card-group>
            <b-card>
                <b-card-header v-b-toggle="'favorite-requests-collapse'">
                    Favorite requests
                </b-card-header>
                <b-collapse id="favorite-requests-collapse">
                    <b-card-body>
                        <div v-if="Requests.length > 0" v-for="(req, ind) in Requests" :key=ind>
                            <b-row>
                                <router-link :to="GetReqPath(req)">{{req}}</router-link>
                                <b-btn size="sm" variant="danger" @click="DelReq(req)">
                                    delete
                                </b-btn>
                            </b-row>
                            <hr>
                        </div>
                        <div v-else>
                            No favorite requests. 
                        </div>
                    </b-card-body>
                </b-collapse>
            </b-card>
             <b-card>
                <b-card-header v-b-toggle="'favorite-documents-collapse'">
                    Favorite requests
                </b-card-header>
                <b-collapse id="favorite-documents-collapse">
                    <b-card-body>
                        <div v-if="Documents.length > 0" v-for="(doc, ind) in Documents" :key=ind>
                            <router-link :to="GetDocPath(doc)">{{doc}}</router-link>
                            
                            <hr>
                            <b-btn size="sm" variant="danger" @click="DelRoc(doc)">
                                delete
                            </b-btn>
                        </div>
                        <div v-else>
                            No favorite requests. 
                        </div>
   
                    </b-card-body>
                </b-collapse>
            </b-card>
        </b-card-group>
    </b-container>
</template>


<script>
import router_urls from '../../consts/router_url.js'
import StoreConsts from '../../consts/store_consts.js'

export default {
    name: 'UserFavoritesView',
    computed:{
        Requests: function(){
            return this.$store.getters.favoriteRequests; 
        },
        Documents: function(){
            return this.$store.getters.favoriteDocuments; 
        }
    },
    methods:{
        GetReqPath: function (req) {
            return `${router_urls.Search}/${req}`;
        },
        GetDocPath: function (req) {
            return `document/${req}`;
        },
        DelReq: function(req){
            this.$store.commit(StoreConsts.DELETE_FAVORITE_REQ, req);
        },
        DelDoc: function(doc){
            this.$store.commit(StoreConsts.DELETE_FAVORITE_DOC, doc);
        }

    },

}
</script>



<style>

</style>


