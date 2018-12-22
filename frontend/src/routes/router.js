import VueRouter from 'vue-router';
import HomePage  from '../components/HomePage.vue';
import DocumentView from '../components/views/DocumentView.vue';
import Search from '../components/SearchSubcomponents/Search.vue';
import SignUpForm from '../components/Auth/SignUpForm.vue';
import UserFavoritesView from '../components/views/UserFavoriteView.vue';
import AddFavoriteForm from '../components/AddFavoriteForm.vue';
import PageNotFound from '../components/PageNotFound.vue';

import urls from '../consts/router_url.js';

var routes = [
    {path: urls.HomePage, component: HomePage},
    {   name: 'document',
        path: `${urls.Document}/:doc_id/:hash`,
        component: DocumentView,
       
    },
    {
        path: `${urls.Search}/:request`,
        component: Search,
    },
    {
        path: '/search/',
        redirect: '/search/ '
    },
    {
        path: urls.SignUp,
        component: SignUpForm,
    },
    {
        path: urls.UserFavorites,
        component: UserFavoritesView,
    },
    {
        path: `${urls.AddFavorite}/:target`,
        component: AddFavoriteForm,
        props: {init_target: 'route', mode: 'new'}
        
    },
    {
        path: `${urls.AddFavorite}/:target/:body`,
        component: AddFavoriteForm,
        props: {init_target: 'route', mode: 'edit'}
        
    },
    {
        path: urls.PageNotFound,
        component: PageNotFound
    }
];


var router = new VueRouter({
    routes: routes
});

export default {Router: router};




