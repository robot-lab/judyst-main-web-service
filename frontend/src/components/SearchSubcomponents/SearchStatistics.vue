<template>
    <b-card >
        <!-- <p>{{tmp}}</p> -->
            <b-card-header v-b-toggle="'search-request-statistics'" class="bg-info text-white">
                Статистический анализ запроса
            </b-card-header>
            <b-collapse id="search-request-statistics">
                <b-card-body>
                    <p>Найдено: {{LinksCount}}</p>
                </b-card-body>
            </b-collapse>
        </b-card>
</template>


<script>
export default {
    name: "SearchStatistics",
    data: function(){
        return{
            tmp: 'none',
        }
    },
    props:
    {
        SearchResults: Array,
        Count: Number,

    },
    computed:{
       LinksCount: function () {
        
            if (this.Count == undefined)
            {
                this.ComputeCount();
            }
            return this.Count; 
            
        },
    },
    methods:{
        ComputeCount: function()
        {
            var acum = 0;
            for (var i = 0; i < this.SearchResults.length; i++)
            {
                acum += this.SearchResults[i].Size;
            }
            this.Count = acum; 
        },
        
    }
}
</script>


<style scoped>

</style>


