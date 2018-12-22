import Vuex from 'vuex'
import Vue from 'vue'
import fav_store from '../src/stores/favorites_store.js';
import store_consts from '../src/consts/store_consts.js';
import utils from './utils.js';


Vue.use(Vuex);
const count = 10;
const test_string_size = 20;
describe('simple_store_test', ()=>{
    const store = new Vuex.Store(fav_store);
    it('just  set and get', ()=>{
        const req ='*->*';
        const model = {caption:'caption', description:'description', body: req};
        store.commit(store_consts.NEW_FAVORITE_REQ, {req, model});
        expect(store.getters.getFavoriteRequest(req)).toEqual(model);
    });
    it('update test', ()=>{
        const updaters = [];
        for (let i = 0; i < count; i ++)
        {
            
            const updater = {flag: false, Update: function(){this.flag = true;}};
            store.commit(store_consts.SET_ON_FAVORITE_UPDATE, updater);
            updaters.push(updater);
        }
        store.dispatch(store_consts.UPDATE_UPDATABLE);
        for (let i = 0; i < count; i++)
        {
            expect(updaters[i].flag);
        }
    })

    it('multiple set, edit and get tests', ()=>{
        const requests = [];
        const documents = [];
        for (let i = 0; i < count; i++)
        {
            let req = utils.GetRandomStr(test_string_size);
            const request ={req, model:{caption:utils.GetRandomStr(test_string_size),
                                        description:utils.GetRandomStr(test_string_size),
                                        body: req}};
            req = utils.GetRandomStr(test_string_size);
            const document ={req, model:{caption:utils.GetRandomStr(test_string_size),
                description:utils.GetRandomStr(test_string_size),
                title: utils.GetRandomStr(test_string_size),
                body: req}};
            requests.push(request);
            documents.push(document);
            store.commit(store_consts.NEW_FAVORITE_DOC, document);
            store.commit(store_consts.NEW_FAVORITE_REQ, request);
            expect(store.getters.getFavoriteRequest(request.req)).toEqual(request.model);
            expect(store.getters.getFavoriteDocument(document.req)).toEqual(document.model);
        }
        

        for (let i = 0; i < count; i++)
        {
            let old_req = requests[i].req;
            let req = utils.GetRandomStr(test_string_size);
            const request ={old_req, model:{caption:utils.GetRandomStr(test_string_size),
                                        description:utils.GetRandomStr(test_string_size),
                                        body: req}};
            old_req = documents[i].req;
            req = utils.GetRandomStr(test_string_size);
            const document ={old_req, model:{caption:utils.GetRandomStr(test_string_size),
                description:utils.GetRandomStr(test_string_size),
                title: utils.GetRandomStr(test_string_size),
                body: req}};
            
            store.commit(store_consts.EDIT_FAVORITE_DOC, document);
            store.commit(store_consts.EDIT_FAVORITE_REQ, request);
            expect(store.getters.getFavoriteRequest(request.model.body)).toEqual(request.model);
            expect(store.getters.getFavoriteDocument(document.model.body)).toEqual(document.model);
            request.req = request.model.body;
            document.req = document.model.body;
            documents[i] = document;
            requests[i] = request; 
            store.commit(store_consts.DELETE_FAVORITE_DOC, documents[i]);
            store.commit(store_consts.DELETE_FAVORITE_REQ, requests[i]);
            expect(store.getters.getFavoriteDocument(documents[i].req)).toBeNull();
            expect(store.getters.getFavoriteRequest(requests[i].req)).toBeNull();
        }





    });
});