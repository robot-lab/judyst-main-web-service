<template>
<b-navbar toggleble="sd"  fixed="top" type="dark" variant="dark"  class = "navbar-main">
  <div class="navbar-header">
    <router-link :to="'/'" class="navbar-brand">Judyst</router-link>
  </div>
    <b-navbar-nav class="nav-item-wrapper">
      <b-nav-item :to="'/search/'">Search</b-nav-item>
    </b-navbar-nav> 

     <b-navbar-nav class="nav-item-wrapper">
      <b-nav-item :to="favoritesUrl">Favorites</b-nav-item>
     </b-navbar-nav> 
     <b-navbar-nav class="nav-item-wrapper">
      <b-nav-item v-b-modal.FavoriteModal>
        <i class="far fa-eye"></i>
      </b-nav-item>
     </b-navbar-nav> 
    <b-navbar-nav class="ml-auto">
    </b-navbar-nav>
    
    <b-navbar-nav v-if="isAuthenticated" class="nav-item-wrapper">
      <b-nav-item @click="logout()">Sign out</b-nav-item>
    </b-navbar-nav>
    <b-navbar-nav class="nav-item-wrapper" v-if="!isAuthenticated">
      <b-nav-item v-b-modal.signInModal>Sign In</b-nav-item>
    </b-navbar-nav> 
    <b-navbar-nav class="nav-item-wrapper" v-if="!isAuthenticated">
      <b-nav-item :to="signUpUrl">Sign Up</b-nav-item>
    </b-navbar-nav> 

    <b-modal id="FavoriteModal" ref="FavoriteModalRef" hide-footer hide-title>
      <user-favorites-view :isModal="true"/>
    </b-modal>
    <b-modal id="signInModal" ref="signInModalRef" hide-footer hide-title>
      <sign-in-form/>
    </b-modal>

      
</b-navbar>
</template>

<script>
import UserFavoritesView from './views/UserFavoriteView';
import router_urls from '../consts/router_url.js'
import StoreConst from '../consts/store_consts.js'
import SignInForm from './Auth/SignInForm'


export default {
    name: 'Navbar',
    data: function () {
    return {
          signUpUrl: router_urls.SignUp,
          favoritesUrl: router_urls.UserFavorites,
      };
   },
    computed:
    {
        isAuthenticated: function(){
           return this.$store.getters.isAuthenticated; 
        },
    },
    methods: {
        logout: function () {
            this.$store.dispatch(StoreConst.AUTH_LOGOUT)
            .then(() => {
                this.$router.push('/');
            })
        },
   
    },
    watch:{
        isAuthenticated: function () {
          if (this.isAuthenticated)
             this.$refs.signInModalRef.hide();
        
      }
    },
    components:{
      UserFavoritesView,
      SignInForm
    }
  }
</script>


<style scoped>
.navbar-main {
  overflow: hidden;
}

.nav-item-wrapper{
  margin-right: 1%;
  margin-left: 1%;
}

</style>
