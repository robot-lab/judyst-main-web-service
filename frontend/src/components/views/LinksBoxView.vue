<template>
<div class="links-block" >
        <div v-for="Link in Links" :key="Link.id">
            <LinkView v-bind:CleanLink="Link.Link" />
        </div>
</div>
</template>


<script>
import LinkView from './LinkView.vue'
export default {
    name: "LinksBoxView",
    components:
    {
        LinkView,

    },
    props:
    {
        Links: Array,
    }
}
</script>
<style scoped>

</style>

