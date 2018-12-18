<template>
    <form>
        <div v-if="isAuthenticated">
        <b-btn size="sm" variant="outline-success">
            Logout
        </b-btn>
        </div>
        <div v-else>
            <b-btn size="sm" variant="outline-success" v-b-modal.signInModal>
                Sign in
            </b-btn>
            
            <b-btn size="sm" variant="outline-success" :to="signUpUrl">
                Sign up
            </b-btn>
            
        </div>
        <b-modal id="signInModal"  hide-footer hide-title>
                <SignInForm/>
        </b-modal>
    </form>
</template>


<script>
import {AUTH_LOGOUT} from './../../utils/auth_const.js';
import SignInForm from './SignInForm.vue';
import router_urls from '../../utils/router_url.js';

export default {
    name: 'AuthBar',
    data: function () {
      return {
            signUpUrl: router_urls.SignUp,
        };
    },
    computed:
    {
        isAuthenticated: function(){
           return this.$store.isAuthenticated; 
        },
    },
    methods: {
        logout: function () {
            this.$store.dispatch(AUTH_LOGOUT)
            .then(() => {
                this.$router.push('/login')
            })
        },
    },
    components:{
        SignInForm,
    }
}
</script>
