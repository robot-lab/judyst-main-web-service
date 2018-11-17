<template>
   <LinkView :CleanLink="CleanLink"/>
</template>


<script>
import LinkView from '../views/LinkView.vue'
    export default 
    {
        name: "SearchResult",
        components:{
            LinkView,
        },
        props: {
            CleanLink: Object
        },
        computed: {
           
        },
        methods:
        {
        
        }

    }
</script>


<style scoped>

</style>
-