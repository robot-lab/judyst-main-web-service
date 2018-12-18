
import {
        NEW_SEARCH_REQUEST,
        NEW_SEARCH_RESULT,
        }
from '../utils/searchHistoryConsts.js'

const state = {
    lastSearch : null,
}

const getters = {
    lastSearchRequest: function (state) {
        if (state.lastSearch != null)
            return state.lastSearch.Request; 
        else 
            return null;
        
    },

    lastSearchResult: function (state) {
        if (state.lastSearch != null)
            return state.lastSearch.Result; 
        else 
            return null;
        
    }

}

const mutations = {
    [NEW_SEARCH_REQUEST]: (state, request)=>
    {
        if (state.lastSearchRequest != null)
        {
            state.lastSearchRequest = null;
        }

        state.lastSearchRequest = {
            Request: request,
            Result: null
        };
    },

    [NEW_SEARCH_RESULT]: (state, request, result) =>
    {
        if (state.lastSearchRequest != null)
        {
            state.lastSearchRequest = null;
        }

        state.lastSearchRequest = {
            Request: request,
            Result: result,
        };
    }

}

const actions = {


}


export default {
    state,
    getters,
    mutations,
    actions
};