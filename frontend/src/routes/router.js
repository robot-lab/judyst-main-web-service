import VueRouter from 'vue-router';
import HomePage  from '../components/HomePage.vue';
import DocumentView from '../components/views/DocumentView.vue';
import Search from '../components/SearchSubcomponents/Search.vue';

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
];


var router = new VueRouter({
    routes: routes
});

export default {Router: router};




