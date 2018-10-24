<template>
    <div class = "search-result-block">
        <div v-for="Link in Links" :key="Link.id">
            <SearchResult v-bind:CleanLink="Link.Link" />
        </div>
    </div>
</template>


<script>
import SearchResult from "./SearchResult.vue"

 export default {
    name: 'SearchResultBlock',
    props: {
        Links:Array
    },
    components: {
        SearchResult
    },
    
 }
    
</script>
<style scoped>
.search-result-block{
  overflow: auto;
  top: 35%;
  left: 15%;
  width:70%;
  height: 58%;
  position: fixed;
  background-color: #EBEBEB
}
</style>