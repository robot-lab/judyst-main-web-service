<template>
<div>
    <div class="col-12">
        <i :class="state" v-b-modal.SaveRequestModal @click="isSaveModalVisible = true"></i>
    </div>
    <b-modal v-model="isSaveModalVisible" id="SaveRequestModal" hide-footer title="Запомнить запрос">
             <form  @submit.prevent="AddReqToFavorites">
                <label>Запрос: {{Request}}</label>
                <div class="form-group">
                    <label class="sr-only">Название</label>
                    <input v-model="caption" type="text" class="form-control"  placeholder="Название"  required>
                </div>
                <div class="form-group">
                    <label  class="sr-only">Комментарий</label>
                    <input v-model="description" type="text" class="form-control"  placeholder="Комментарий" >
                </div>
                <div class="form-group">
                    <b-btn type="submit" size="sm" class="submit-btn" variant="outline-success">Сохранить</b-btn>
                </div>
             </form>
    </b-modal>
</div>
</template>

<script>
import StoreConsts from '../../consts/store_consts.js';
export default {
    name: "SearchRequestManager",
    props:
    {
        Request: String,
        
    },
    data: ()=>{return{
        caption: '',
        description: '',
        isSaveModalVisible: false,
        salt:''
    }},
    computed:
    {
        state: function(){
            let req = this.Request.trim(); 
            if (this.salt != '')
                return'';
            if (this.$store.getters.getFavoriteRequest(req) === null)
                return 'far fa-star';
            else 
                return 'fas fa-star';
        }
    },
    methods:{
          AddReqToFavorites: function() {
            let req = this.Request.trim();
            if (req == '')
                return;

            let model = {
                caption : this.caption,
                description : this.description,
                body: req
            };
            this.$store.commit(StoreConsts.NEW_FAVORITE_REQ, {req, model});
            this.isSaveModalVisible = false;
            this.salt = 'reinvoking';
            this.salt = '';

        },  
    }

}
</script>

<style scoped>
.color-stat-white{
    color: #aaaaaa; 
}

.color-stat-gold{
    color: gold; 
}
</style>
