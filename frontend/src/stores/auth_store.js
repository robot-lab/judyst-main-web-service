import axios from 'axios';
// import auth0 from 'auth0-js';

import {
    AUTH_REQUEST,
    AUTH_SUCCESS,
    AUTH_ERROR, 
    AUTH_LOGOUT,
    REGISTER_SUCCESS,
    REGISTER_REQUEST,
    REGISTER_ERROR
        }   
    from '../utils/auth_const.js';
import urls from '../utils/urls.js';



const state = {
    token: localStorage.getItem('user-token') || '',
    status: '',
    // auth,

  };


const getters = {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
}


const actions = {
 // eslint-disable-next-line 
    [AUTH_REQUEST]: ({commit, dispatch}, user) => {
      return new Promise((resolve, reject) => { // The Promise used for router redirect in login
        commit(AUTH_REQUEST);
        axios({url: urls.Auth_signin, data: user, method: 'POST' })
          .then(resp => {
            // console.log(resp);
            const token = resp.data.token;
            if (token === undefined){
                throw 'Token is undefined';
            }
            localStorage.setItem('user-token', token) // store the token in localstorage
            axios.defaults.headers.common['Authorization'] = 'Token ' +  token;
            commit(AUTH_SUCCESS, token)
            // dispatch(USER_REQUEST);
            resolve(resp);
          })
        .catch(err => {
          commit(AUTH_ERROR, err)
          localStorage.removeItem('user-token') ;// if the request fails, remove any possible user token if possible
          reject(err);
        })
      })
    },

 // eslint-disable-next-line 
    [AUTH_LOGOUT]: ({commit, dispatch}) => {
         // eslint-disable-next-line 
        return new Promise((resolve, reject) => {
          commit(AUTH_LOGOUT);
          axios({url: urls.Auth_signout, method: 'GET' });
          localStorage.removeItem('user-token'); // clear your user's token from localstorage
          delete axios.defaults.headers.common['Authorization'];
            
          resolve();
        })
      }, 


 // eslint-disable-next-line 
    [REGISTER_REQUEST]: ({commit, dispatch}, user) => {
        return new Promise((resolve, reject) => {
            commit(REGISTER_REQUEST);
            axios({url: urls.Auth_signup, data: user, method: 'POST' })
            .then(resp => {
              const token = resp.data.token;
              localStorage.setItem('user-token', token) // store the token in localstorage
              axios.defaults.headers.common['Authorization'] = token;
              commit(REGISTER_SUCCESS, token);
            //   dispatch(USER_REQUEST);
              resolve(resp);
            })
          .catch(err => {
            commit(REGISTER_ERROR, err);
            localStorage.removeItem('user-token'); // if the request fails, remove any possible user token if possible
            reject(err);
          })
        }); 
    },


  };



const mutations = {
    [AUTH_REQUEST]: (state) => {
        state.status = 'loading';
    },
    [AUTH_SUCCESS]: (state, token) => {
        state.status = 'success';
        state.token = token;
    },
    [AUTH_ERROR]: (state) => {
        state.status = 'error';
    },
    [REGISTER_REQUEST]: (state) => {
        state.status = 'loading';
    },
    [REGISTER_SUCCESS]: (state, token) => {
        state.status = 'success';
        state.token = token;
    },
    [REGISTER_ERROR]: (state) => {
        state.status = 'error';
    },
}

export default {
    state,
    getters,
    mutations,
    actions
};