import VueRouter from 'vue-router';
import HomePage  from '../components/HomePage.vue';
import DocumentView from '../components/views/DocumentView.vue';
import Search from '../components/SearchSubcomponents/Search.vue';
import SignUpForm from '../components/Auth/SignUpForm.vue';

import urls from '../utils/router_url.js';

var routes = [
    {path: '/', component: HomePage},
    {   name: 'document',
        path: '/document/:doc_id/:hash',
        component: DocumentView,
       
    },
    {
        path: '/search/:request',
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
];


var router = new VueRouter({
    routes: routes
});

export default {Router: router};




