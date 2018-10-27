import VueRouter from 'vue-router';
import HomePage  from '../components/HomePage.vue';



var routes = [
    {path: '/', component: HomePage},
];


var router = new VueRouter({
    routes: routes
});

export default {Router: router};




