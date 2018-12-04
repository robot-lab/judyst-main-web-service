<template>
    <div class= "link-container container card">
        <b-card-header class="link-header">
            <span> 
                <p>Цитирующий документ: <router-link class="link" :to="`/document/${utils.StashDocId(CleanLink.doc_id_from)}/0`">{{CleanLink.doc_id_from}}</router-link></p>
            </span>
            <span>
                <p>Цитируемый документ: <router-link class="link" :to="`/document/${utils.StashDocId(CleanLink.doc_id_to)}/0`">{{CleanLink.doc_id_to}}</router-link></p>
            </span>
        <!-- <b-btn variant="outline-success sm-12" v-b-toggle="TitleId + '_main'" class="main-toggler" >Свернуть</b-btn> -->
        </b-card-header>
        <b-card-body>
            <!-- <b-collapse :visible="DefaultCollapse" :id="TitleId + '_main'"> -->
                    <p>
                        <b>Заголовок цитируемого документа:</b> {{CleanLink.to_doc_title}}
                    </p>
                    <span> <p>Количество упоминаний: {{CleanLink.citations_number}} </p></span>
                    <a v-b-toggle="TitleId" v-b-tooltip.hover title="Нажмите, чтобы просмотреть контекст цитаты" class="context-toggler">
                        Контекст цитирования
                    </a>
                    <b-collapse :id="TitleId">
                    <b-card-group v-for="i in CitationsRange" :key="i">
                        <b-card>
                            <b-card-header>
                            </b-card-header>
                            <b-card-body>
                                <p>{{CleanLink.contexts[i].before}} <b>{{CleanLink.contexts[i].citation}}</b> {{CleanLink.contexts[i].after}} </p>
                            </b-card-body>
                            <b-card-footer>
                            <router-link :to="`/document/${utils.StashDocId(CleanLink.doc_id_from)}/${utils.HashLink(CleanLink)}`">
                                Перейти к цитате в тексте
                            </router-link>
                            </b-card-footer>
                        </b-card>
                    </b-card-group>
                    </b-collapse>
            <!-- </b-collapse> -->
        </b-card-body>
    </div>
</template>


<script>
import utils from '../../utils/common.js'

export default {
    name: 'LinkView',
    props: {
            CleanLink: Object,
            DefaultCollapse: Boolean,
    },
    data: function () {
        return {
            utils: utils,
        }
    },
    computed: {
        /*CleanLink: function() {
            var str = this.Link.json;
            return JSON.parse(str);
        },*/
        CitationsRange : function()
        {
            var ret = []
            for(var i=0; i< this.CleanLink.citations_number; i++)
                ret.push(i)      
            return ret
        },
        TitleId: function () {
            return '#collapse' + '_' + this.CleanLink.doc_id_from + '-' + this.CleanLink.doc_id_to;
        }
    },
    methods:
    {
        GetPositionLink: function (id, pos) {
            return '#' + id + "__" + pos
        }, 

        
    }

}
</script>

<style>
.link-container{
  z-index: 2;
  width: 100%;
  padding-left: 3%;
  padding-right: 3%;
  overflow: hidden;
  word-wrap: break-word; 
  margin-bottom: 5%;
  
}
.context-toggler{
    border: 1px solid #ddd; 
    background: #fff;
    padding: 10px;
    vertical-align: middle;
    text-align: center;
    cursor: pointer;
}

.main-toggler{
    cursor: pointer;
}


</style>




