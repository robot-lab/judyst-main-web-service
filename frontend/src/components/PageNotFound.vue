<template>
    <b-container>
        <b-card>
            <b-card-body class="card-body">
            <h1>This page not found.</h1>
            <h3><i>You can go to</i></h3>
            <ul>
            <li><router-link :to="HomePage">Home page</router-link></li>
            <li><router-link :to="Search">Search</router-link></li>
            <li><router-link :to="Favorites">Favorite requests and documents</router-link></li>
            </ul>
            </b-card-body>
        </b-card>
    </b-container>
</template>

<script>
import urls from '../consts/router_url.js';
export default {
    name: "PageNotFound",
    data: ()=>{return {
        HomePage: urls.HomePage,
        Search: urls.Search,
        Favorites: urls.UserFavorites
    }}
}
</script>

<style>
.card-body{
    width:80%;
}
</style>

