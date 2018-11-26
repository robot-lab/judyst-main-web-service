<template>
    <div class= "container link-container card card-body">
        <span> 
            <p>Цитирующий документ: <router-link :to="`/document/${utils.StashDocId(CleanLink.doc_id_from)}/0`">{{CleanLink.doc_id_from}}</router-link></p>
        </span>
        <span>
            <p>Цитируемый документ: <router-link :to="`/document/${utils.StashDocId(CleanLink.doc_id_to)}/0`">{{CleanLink.doc_id_to}}</router-link></p>
        </span>
        <span>
            <p>
                Заголовок цитируемого документа: {{CleanLink.to_doc_title}}
            </p>
        </span>
        <span> <p>Количество упоминаний: {{CleanLink.citations_number}} </p></span>
        <div v-for="i in CitationsRange" :key="i">
           <span> <p>Контекст цитаты: {{CleanLink.contexts[i].before}} <b>{{CleanLink.contexts[i].citation}}</b> {{CleanLink.contexts[i].after}} </p></span>
           <router-link :to="`/document/${utils.StashDocId(CleanLink.doc_id_from)}/${utils.HashLink(CleanLink)}`">
                Перейти к цитате в тексте
            </router-link>
        </div>
        <!-- <p>{{CleanLink}}</p> -->
    </div>
</template>


<script>
import utils from '../../utils/common.js'

export default {
    name: 'LinkView',
    props: {
            CleanLink: Object
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
  margin-bottom: 10%;
  
}
</style>




