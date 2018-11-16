<template>
   <div class= "container link-container card card-body">
        <span> <p>Цитирующий документ: {{CleanLink.doc_id_from}} </p></span>
        <span> <p>Цитируемый документ: {{CleanLink.doc_id_to}} </p></span>
        <span> <p>Заголовок цитируемого документа: {{CleanLink.to_doc_title}} </p></span>
        <span> <p>Количество упоминаний: {{CleanLink.citations_number}} </p></span>
        <div v-for="i in CitationsRange" :key="i">
           <span> <p>Контекст цитаты: {{CleanLink.contexts[i].before}} <b>{{CleanLink.contexts[i].citation}}</b> {{CleanLink.contexts[i].after}} </p></span>
           <a href="#">Перейти к цитате в тексте</a>
        </div>
        <!-- <p>{{CleanLink}}</p> -->
    </div>
</template>


<script>
    export default 
    {
        name: "SearchResult",
        props: {
            CleanLink: Object
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
            }
        },
        methods:
        {
            GetPositionLink: function (id, pos) {
                return '#' + id + "__" + pos
            } 
        }

    }
</script>


<style scoped>
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
