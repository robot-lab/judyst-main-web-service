<template>
    <div class="text-center " style="padding:50px 0">
	<div class="login-form-1">
		<form class="text-left"  @submit.prevent="submit">
			<div class="login-form-main-message"></div>
			<div class="main-login-form">
            <div class="login-group">
                <div class="form-group" >
                    <label for="lg_email" class="sr-only" v-if="target == 'request'">Запрос</label>
                    <label for="lg_email" class="sr-only" v-else>Номер документа</label>
                    <input v-model="body" type="text" class="form-control"  :placeholder="bodyPlaceholder" required>
                </div>
                <div class="form-group">
                    <label for="lg_password" class="sr-only">Название</label>
                    <input v-model="caption" type="text" class="form-control"  placeholder="Название"  required>
                </div>
                <div class="form-group">
                    <label for="lg_email" class="sr-only">Комментарий</label>
                    <input v-model="description" type="text" class="form-control"  placeholder="Комментарий" >
                </div>
                <div class="form-group">
                    <div >
                        <b-btn type="submit" size="sm" class="submit-btn" variant="outline-success">Сохранить</b-btn>
                    </div>
                    <div v-if="mode=='edit'">
                        <b-btn  size="sm" class="submit-btn" variant="outline-success" @click="abort()">Отменить</b-btn>
                    </div>
				</div>
			</div>
			</div>
		</form>
	</div>
</div>
</template>


<script>
import StoreConsts from '../consts/store_consts.js';
import urls from '../consts/router_url.js';
import router_url from '../consts/router_url.js';
import utils from '../utils/common.js';

const possible_targets = ['request', 'document'];
const possible_mods = ['new', 'edit'];

export default {
    name: "AddFavoriteForm",
    props:
    {
        init_target: String,
        mode: String, 
        model: String,
        isModal: Boolean

    },
    data:()=>
    { return {
        body: '',
        oldBody: '',
        caption: '',
        description: '',
        target:'',
        Modal: false,
    }},
    computed:{
        bodyPlaceholder: function (){
            if (this.target == 'request')
                return "Поисковый запрос"; 
            else
                return "Номер документа";
        }  
    },
    methods:
    {
        abort: function()
        {
            this.$emit("Abort");
            this.$emit("Finish");

            this.$router.push(router_url.UserFavorites);
        },
        submit: function () {
            let model = {caption: this.caption,
                         description: this.description,
                         body: this.body};

            let name = '';
            let req = '';
            if (this.target == "request")
                if (this.mode == 'edit')
                {
                    name = StoreConsts.EDIT_FAVORITE_REQ;
                    req = this.oldBody;
                }
                else
                {
                    name = StoreConsts.NEW_FAVORITE_REQ;
                    req = this.body;
                }
            else
                if (this.mode == 'edit')
                {
                    name = StoreConsts.EDIT_FAVORITE_DOC;
                    req = this.oldBody;

                }
                else
                {
                    name = StoreConsts.NEW_FAVORITE_DOC;
                    req = this.body;
                }
            this.$store.commit(name, {req, model});
            this.oldBody = "";
            this.body = "";
            this.caption = "";
            this.description = "";
            this.$emit('Finish');
            this.$store.dispatch(StoreConsts.UPDATE_UPDATABLE);
            if (!this.Modal)
                this.$router.push(router_url.UserFavorites);
        
        }
    },
   created: function () {
       let model = null; 
        if (this.init_target == 'route')
        {
            this.target = this.$route.params.target; 
            if (this.mode == 'edit')
            {
                let req = this.$route.params.body;

                if (this.target == 'request')
                {
                    req = utils.DeStashRequest(req);
                    model = this.$store.getters.getFavoriteRequest(req);

                }
                else
                {
                    req = utils.DeStashDocId(req);
                    model = this.$store.getters.getFavoriteDocument(req);
                    
                }
                if (model == null)
                    this.$router.push(router_url.PageNotFound);
            }
        }
        else
        {
            this.target = this.init_target;
        }

        if (this.target != undefined && this.mode != undefined &&
            (possible_targets.indexOf(this.target) == -1||
            possible_mods.indexOf(this.mode) == -1))
                this.$router.push(urls.PageNotFound);
       
       if (this.model || model != null)
        {
            if (model == null)
                model == this.model;

            this.caption = model.caption;
            this.description = model.description; 
            this.body = model.body;
            if (this.mode == 'edit')
                this.oldBody = this.body; 
        }

        if (this.isModal)
            this.Modal = this.isModal;
            
    }
}
</script>

<style scoped>
.submit-btn{
    margin:1%;
}
</style>
