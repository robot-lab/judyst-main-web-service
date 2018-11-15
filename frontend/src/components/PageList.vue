<template>
<div class="page-list">

<span>
    <a v-for="range in PageLinkList" :key="range[0]" 
                v-on:click="$emit('PageChanged', range)"
                class="page-link">
        
        |{{range[0]}} - {{range[1]}}|
    
    </a>
    </span>    
</div>
</template>




<script>
export default 
{
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
            ret.push([curr, this.Count])
            return ret
        },
        
        
    }
    
 }

 </script>

 <style scoped>
 .page-list{
     background-color: #FCFCFC;
     margin-bottom: 2%;
 }
 .page-link{
    font-size:16px; color:#0000ff; font-weight:bold
 }
.page-link:hover {
    font-size:16px; color:#0000ff; font-weight:bold
}
 </style>
 