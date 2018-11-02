<template>
<div>
<p>I'm here</p>
<span> <a v-for="range in PageLinkList" :key="range[0]" v-on:click="$emit('PageChanged', range)"> </a></span>    
</div>
</template>





<script>

 export default {
    name: 'PageList',
    props: {
        Count: Number,
        Step: Number,
        Current: Array

    },
    computed:
    {
        PageLinkList : function () {
            var ret = [];
            var curr = 1;
            var next = curr + this.Step;
            while (next < this.Count)
            {
                ret.push([curr, next]);
                curr = next + 1
                next += this.Step + 1
            }
            ret.push(curr, this.Count)
            return ret
        },
        
        
    },
    
 }