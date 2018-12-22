<template>
<div>
    <div class="col-12">
        <i :class="state" @click="starOnClick()"></i>
    </div>
    <b-modal v-model="isSaveModalVisible" id="SaveModal" hide-footer title="Запомнить запрос">
             <form  @submit.prevent="submit">
                <label>{{Target=='document'?'Номер документа':'Запрос'}}: {{Request}}</label>
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
import StoreConsts from '../consts/store_consts.js';

// const possible_targets = ['document', 'request'];

export default {
    name: "SearchRequestManager",
    props:
    {
        Request: String,
        Target: String,
        Title: String
    },
    data: ()=>{return{
        caption: '',
        description: '',
        isSaveModalVisible: false,
        submit: null,
        salt:''
    }},
    computed:
    {
        isFavorite: function (){
              if (this.salt != '')
                return'';
            const req = this.Request.trim(); 
            const part1 = (this.Target == 'document' &&
                this.$store.getters.getFavoriteDocument(req) !== null);

            const part2 = (this.Target == 'request' &&
                this.$store.getters.getFavoriteRequest(req) !== null );
            const ret = part1 || part2;
                
            return ret;
        },
        state: function(){
          
            if(!this.isFavorite)
                return 'far fa-star';
            else 
                return 'fas fa-star';
        },
        starOnClick: function(){
            if (!this.isFavorite)
                // eslint-disable-next-line 
                return function () {this.isSaveModalVisible = true; }
            else return function (){
                const name = this.Target == 'document'?StoreConsts.DELETE_FAVORITE_DOC:StoreConsts.DELETE_FAVORITE_REQ;
                const req = this.Request.trim(); 
                this.$store.commit(name, {req});
            };                 
                    
        },

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
        AddDocToFavorites: function() {
            let req = this.Request.trim();
            if (req == '')
                return;

            let model = {
                caption : this.caption,
                description : this.description,
                title: this.title,
                body: req
            };
            this.$store.commit(StoreConsts.NEW_FAVORITE_DOC, {req, model});
            this.isSaveModalVisible = false;
            this.salt = 'reinvoking';
            this.salt = '';

        }, 
    },
    created: function(){
        if (this.Target == 'document')
            this.submit = this.AddDocToFavorites;
        else
            this.submit = this.AddReqToFavorites;
        

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
