<template>
<div class="page-list">
<!-- <p>{{tmp}}</p> -->
<span>
    <a v-on:click="$emit('PageChanged', FirstPages)" class="page-link">
         &lt;&lt;&lt;
    </a>


    <a v-for="range in PrevioslyPages" :key="range[0]" 
                v-on:click="$emit('PageChanged', range)"
                class="page-link">
        {{range[0]}} - {{range[1]}}
    </a>

    <p  class="page-link current-link">
        |{{Current[0]}} - {{Current[1]}}|
    </p>

    <a v-for="range in NextPages" :key="range[0]" 
                v-on:click="$emit('PageChanged', range)"
                class="page-link">
        {{range[0]}} - {{range[1]}}
    </a>


    <a v-on:click="$emit('PageChanged', LastPages)" class="page-link">
        &gt;&gt;&gt;
    </a>


    </span>
        
</div>
</template>




<script>
export default 
{
    name: 'PageList',
    data: function () {
        return {
            tmp: 'none',
        }
    },
    props: {
        Count: Number,
        Step: Number,
        Current: Array

    },
    computed:
    {
        PrevioslyPages: function () {
            // this.tmp = this.Current;
            var ret = [];
            var curr = this.Current; 
            if (curr[0] > 2)
            {
                var min = curr[0] - this.Step - 1; 
                if (min < 1)
                    min = 1;
                ret.push([min, curr[0] - 1]);
            }
            return ret;

        },
        NextPages : function () {
            // var ret = [];
            // var curr = 1;
            // var next = curr + this.Step;
            // while (next < this.Count)
            // {
            //     ret.push([curr, next]);
            //     curr = next + 1
            //     next += this.Step + 1
            // }
            // ret.push([curr, this.Count])
            // return ret
            var ret = [];
            var curr = this.Current; 
           
            for (var i = 0; i < 2; i ++)
            {   var oldCurr = curr;
                curr = [oldCurr[1] + 1, oldCurr[1] + this.Step]
                if (curr[0] > this.Count)
                    break;

                if (curr[1] > this.Count)
                {
                    curr[1] == this.Count; 
                }
                ret.push(curr);
            }
            return ret; 
        },


        FirstPages: function () {
            var ret = [1, this.Step];
            if (ret[1] > this.Count)
                ret[1] = this.Count;
            return ret; 
        },

        LastPages: function () {
            var ret = [this.Count - this.Step + 1, this.Count]
            if (ret[0] < 1)
                ret[0] = 1; 
            return ret; 
        }
        
        
    }
    
 }

 </script>

 <style scoped>
 .page-list{
     background-color: #FCFCFC;
     margin-bottom: 2%;
 
     display: inline-block;
 }
 .page-list a{
     margin-top: 4px; 
 }
 .page-link{
    font-size:16px;
    
    font-weight:bold;
    display: inline;
 }

.current-link{

}
 </style>
 