import VueRouter from 'vue-router';
import HomePage  from '../components/HomePage.vue';
import DocumentView from '../components/views/DocumentView.vue';


var routes = [
    {path: '/', component: HomePage},
    {   name: 'document',
        path: '/document/:doc_id/:hash',
        component: DocumentView,
       
    }
];


var router = new VueRouter({
    routes: routes
});

export default {Router: router};




