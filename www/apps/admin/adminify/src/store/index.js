import Vue from 'vue'
import Vuex from 'vuex'
import menu from '../js/menu'
import config from '../js/config'
import * as api from './apis'
import * as TYPES from './mutation_type'
Vue.use(Vuex)
import createPersistedState from 'vuex-persistedstate'

const store = new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    dark: false,
    pageTitle: 'Home',
    menu: menu,
    user: {},
    token: null,
    message: {
      type: null,
      body: null
    },
    config: config,
    adminContentUrl: {
      href: 'http://www.baidu.com'
    }
  },
  mutations: {
    setAuth(state, { user, token }) {
      state.user = user
      state.token = token
      global.helper.ls.set('user', user)
      global.helper.ls.set('token', token)
    },
    setMenu(state, data) {
      state.menu = data
    },
    setPageTitle(state, data) {
      state.pageTitle = data
    },
    showMessage(state, type, body) {
      state.message = { type, body }
    },
    ON_LOGIN(state, data) {
      state.user = data.user
    },
    ON_LOGOUT(state, data) {
      state.message = { type: 'info', body: data }
    },
    ON_GET_MENU(state, data) {
      state.menu = data.body
    },
    ER(state, data) {
      state.message = { type: 'info', body: data }
    },
    OK(state, data) {
      state.message = { type: 'info', body: data }
    },
    DARK_MODE(state, ifDark) {
      state.dark = ifDark
    },
    CHANGE_ADMIN_CONTENT_URL(state, urlEntry) {
      state.adminContentUrl = Object.assign({}, urlEntry)
    }
  },
  actions: {
    checkAuth({ commit, state }) {
      let data = {
        user: global.helper.ls.get('user'),
        token: global.helper.ls.get('token')
      }
      commit('setAuth', data)
      // return new Promise(function(resolve, reject){
      //   if(state.token==null){
      //     reject('token is null')
      //   }else{

      //     // commit('setAuth', data)
      //   }
      // })
    },
    checkPageTitle({ commit, state }, path) {
      for (let k in state.menu) {
        if (state.menu[k].href === path) {
          commit('setPageTitle', state.menu[k].title)
          break
        }
      }
    },
    DO_GET_MENU({ commit }) {
      return new Promise(function(resolve, reject) {
        api
          .DO_GET_MENU()
          .then(res => {
            if (res.data.ok) {
              commit(TYPES.ON_GET_MENU, res.data)
              resolve(res)
            } else {
              commit(TYPES.OK)
              reject(res)
            }
          })
          .catch(res => {
            commit(TYPES.ER)
            reject(res)
          })
      })
    },
    DO_LOGIN({ commit }, data) {
      return new Promise(function(resolve, reject) {
        api
          .DO_LOGIN(data)
          .then(res => {
            if (res.data.ok) {
              commit(TYPES.ON_LOGIN, res.data)
              resolve(res)
            } else {
              commit(TYPES.ER)
              reject(res)
            }
          })
          .catch(res => {
            commit(TYPES.ER, res.data)
            reject(res)
          })
      })
    },
    DO_LOGOUT({ commit }) {
      return new Promise(function(resolve, reject) {
        api
          .DO_LOGOUT()
          .then(res => {
            if (res.data.ok) {
              commit(TYPES.ON_LOGOUT, res.data)
              resolve(res)
            } else {
              commit(TYPES.ER)
              reject(res)
            }
          })
          .catch(res => {
            commit(TYPES.ER)
            reject(res)
          })
      })
    },
    DO_AUTH_COOKIE_ME({ commit }) {
      return new Promise(function(resolve, reject) {
        api
          .DO_AUTH_COOKIE_ME()
          .then(res => {
            commit(TYPES.OK)
            resolve(res)
          })
          .catch(res => {
            commit(TYPES.ER)
            reject(res)
          })
      })
    }
  }
})

export default store
