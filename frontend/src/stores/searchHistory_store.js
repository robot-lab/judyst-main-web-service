
import {
        NEW_SEARCH_RESULT, NEW_LINKS_PACK,
        }
from '../consts/store_consts';

const state = {
    storedSearch :  {},
    storedLinksPack: {}
}

const getters = {
    getStoredRes: state => req => {
        if (req in state.storedSearch)
            return state.storedSearch[req];
        else
            return null;
    },

    storedResults: state => {
        return state.storedSearch;
    },

    getStoredLinks: state => req => {
        if (req in state.storedLinksPack)
            return state.storedLinksPack[req];
        else
            return null;
    },

    storedLinks: state => {
        return state.storedLinks;
    }


}

const mutations = {

    [NEW_SEARCH_RESULT]: (state, val) =>
    {
       state.storedSearch[val.request] = val.result; 
    },
    [NEW_LINKS_PACK]: (state, val) =>
    {
       state.storedLinksPack[val.request] = val.result; 
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