<template>
<div class="links-block" >
        <div v-for="(Link, ind) in Links" :key="ind">
            <LinkView v-bind:CleanLink="Link" :CollapseDefault="CollapseDefault"/>
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
        CollapseDefault: Boolean,
    }
}
</script>
<style scoped>

</style>

