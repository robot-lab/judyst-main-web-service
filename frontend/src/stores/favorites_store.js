
import {
    NEW_FAVORITE_DOC,
    NEW_FAVORITE_REQ,
    DELETE_FAVORITE_DOC,
    DELETE_FAVORITE_REQ
    }
from '../consts/store_consts';

const state = {
    favoriteRequests:[],
    favoriteDocuments:[],

}

const getters = {
    
    favoriteRequests: state => {
        return state.favoriteRequests;
    },

    favoriteDocuments: state => {
        return state.favoriteDocuments;
    }


}

const mutations = {

    [NEW_FAVORITE_REQ]: (state, val) =>
    {
        if (state.favoriteRequests.indexOf(val) == -1)
            state.favoriteRequests.push(val); 
    },
    [DELETE_FAVORITE_REQ]: (state, val) =>
    {
        const ind = state.favoriteRequests.indexOf(val);
        if (ind != -1)
            state.favoriteRequests.splice(ind, 1);
    },
    [NEW_FAVORITE_DOC]: (state, val) =>
    {
        if (state.favoriteDocuments.indexOf(val) == -1)
            state.favoriteRocuments.push(val); 
    },
    [DELETE_FAVORITE_DOC]: (state, val) =>
    {
        const ind = state.favoriteDocuments.indexOf(val);
        if (ind != -1)
            state.favoriteDocuments.splice(ind, 1);
    },
}

const actions = {


}


export default {
state,
getters,
mutations,
actions
};