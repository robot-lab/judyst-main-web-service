
import {
    NEW_FAVORITE_DOC,
    NEW_FAVORITE_REQ,
    EDIT_FAVORITE_DOC,
    EDIT_FAVORITE_REQ,
    DELETE_FAVORITE_DOC,
    DELETE_FAVORITE_REQ,
    UPDATE_FROM_STORAGE,
    SET_ON_FAVORITE_UPDATE,
    DELETE_ON_FAVORITE_UPDATE
    }
from '../consts/store_consts';

const base_storage = localStorage;

const storage = {
    getItem: (key, prefix) => base_storage.getItem(prefix + key),
    setItem: (key, prefix, val) => base_storage.setItem(prefix + key, val),
    removeItem: (key, prefix) => base_storage.removeItem(prefix + key),
    clear: () => base_storage.clear(),
    key: (ind) => base_storage.key(ind)
}
let isUseStorage = true;

const state = {
    favoriteRequests:{},
    favoriteDocuments:{},
    onFavoriteUpdate:null

}

const getters = {
    
    favoriteRequests: state => {
        return state.favoriteRequests;
    },

    favoriteDocuments: state => {
        return state.favoriteDocuments;
    },

    getFavoriteRequest: state => req => {
        if (req in state.favoriteRequests)
            return state.favoriteRequests[req];
        else
            return null;
    },

    getFavoriteDocument: state => doc_id  =>{
        if (doc_id in state.favoriteDocuments)
            return state.favoriteDocuments[doc_id];
        else
            return null;
    }

}

const mutations = {

    [NEW_FAVORITE_REQ]: (state, val) =>
    {
        state.favoriteRequests[val.req] = val.model; 
        if (isUseStorage)
            storage.setItem(val.req, 'req_', JSON.stringify(val.model));
    },
    [EDIT_FAVORITE_REQ]: (state, val) =>
    {
        let model = state.favoriteRequests[val.req];
        delete state.favoriteRequests[val.req];
        model.body = val.model.body;
        model.caption  = val.model.caption;
        model.description = val.model.description;
        state.favoriteRequests[val.body] = model; 
        if (isUseStorage)
            {
                storage.removeItem(val.req, 'req_');
                storage.setItem(val.req,'req_', JSON.stringify(val.model));
            }
    },
    [DELETE_FAVORITE_REQ]: (state, val) =>
    {
        delete state.favoriteRequests[val.req];
        if (isUseStorage)
            storage.removeItem(val.req, 'req_');

    },
    [NEW_FAVORITE_DOC]: (state, val) =>
    {
        state.favoriteDocuments[val.req] = val.model; 
        if (isUseStorage)
            storage.setItem(val.req, 'doc_', JSON.stringify(val.model));
    },
    [EDIT_FAVORITE_DOC]: (state, val) =>
    {
        let model = state.favoriteDocuments[val.req];
        delete state.favoriteDocuments[val.req];
        model.body = val.model.body;
        model.caption  = val.model.caption;
        model.title  = val.model.title;
        model.description = val.model.description;
        state.favoriteDocuments[val.body] = model; 
        if (isUseStorage)
        {
            storage.removeItem(val.req, 'doc_');
            storage.setItem(val.req, 'doc_', JSON.stringify(val.model));
        }
    },
    [DELETE_FAVORITE_DOC]: (state, val) =>
    {
        delete state.favoriteDocuments[val.req];
        if (isUseStorage)
            storage.removeItem(val.req, 'doc_');
    },
    [SET_ON_FAVORITE_UPDATE]: (state, val) =>
    {
        if (state.onFavoriteUpdate == null)
            state.onFavoriteUpdate = [];
        state.onFavoriteUpdate.push(val); 
    },
    [DELETE_ON_FAVORITE_UPDATE]: (state) =>
    {
        state.onFavoriteUpdate = null; 
    }
}

const actions = {
        // eslint-disable-next-line 
        [UPDATE_FROM_STORAGE]: ({commit, dispatch}) => {
            return new Promise((resolve, reject) => {
                    try
                    {
                        isUseStorage = false;
                        let i = 0;
                        let key = base_storage.key(i);
                        while (key !== null)
                        {
                            const splited_key = key.split('_');
                            const prefix = splited_key[0];
                            if (prefix == 'req' || prefix == 'doc')
                            {
                                const req = splited_key.slice(1, splited_key.length).join('');
                                const name = (prefix == 'req') ? NEW_FAVORITE_REQ : NEW_FAVORITE_DOC;
                                const model = JSON.parse(base_storage.getItem(key));
                                commit(name, {req, model});
                            }
                            i+= 1;
                            key = base_storage.key(i);
                            // console.log(i);
                            // console.log(key);
                            // console.log(base_storage.getItem(key));
                        }
                        resolve();
                        isUseStorage = true;
                    }           
                    catch(e)
                    {
                        isUseStorage = true;
                        reject(e);
                    }
            })
            }, 

}

const updating_mutations = [
    NEW_FAVORITE_DOC,
    NEW_FAVORITE_REQ,
    EDIT_FAVORITE_DOC,
    EDIT_FAVORITE_REQ
]

const plugins = {
    OnFavoriteUpdateEmitter : store => {
        store.subscribe((mutation, state) => {
            if (state.onFavoriteUpdate != null)
                if(updating_mutations.indexOf(mutation.type) != -1)
                {
                        for (let i = 0; i < state.onFavoriteUpdate.length; i++)
                    {
                        state.onFavoriteUpdate[i]();
                    }
    }
        });
      }
};


export default {
state,
getters,
mutations,
actions,
plugins
};