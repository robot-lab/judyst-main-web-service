<template>
   <div class= "container link-container">
        <span> <p>Цитирующий документ: {{CleanLink.doc_id_from}} </p></span>
        <span> <p>Цитируемый документ: {{CleanLink.doc_id_to}} </p></span>
        <span> <p>Заголовок цитируемого документа: {{CleanLink.to_doc_title}} </p></span>
        <span> <p>Количество упоминаний: {{CleanLink.citations_number}} </p></span>
        <div v-for="i in CitationsRange" :key="i">
           <span> <p>Контекст цитаты: {{CleanLink.contexts_list[i]}} </p></span>
           <a href="#">Позиция в тексте</a>
        </div>
        <hr color=#00008B>
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
}
</style>
