import Vue from 'vue'
import Vuex from 'vuex'
import config from '../js/config'
import * as api from './apis'

Vue.use(Vuex)
import createPersistedState from 'vuex-persistedstate'

const store = new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    dark: false,
    article: {
      create: {
        id: null,
        content: '# hello world'
      },
      update: {
        id: null,
        content: '# hello world'
      }
    },
    config: config,
    message: {
      type: null,
      body: null
    }
  },
  mutations: {
    SAVE(state, article) {
      if (article.id) {
        state.article.update = article
      } else {
        state.article.create = article
      }
    },
    ER(state, data) {
      state.message = { type: 'info', body: data }
    },
    OK(state, data) {
      state.message = { type: 'info', body: data }
    }
  },
  actions: {
    SAVE({ commit }, data) {
      return new Promise(function(resolve, reject) {
        api
          .SAVE(data)
          .then(res => {
            if (res.data.ok) {
              commit('OK', res.data.body)
              resolve(res)
            } else {
              commit('ER')
              reject(res)
            }
          })
          .catch(res => {
            commit('ER')
            reject(res)
          })
      })
    },
    PUBLISH({ commit }, data) {
      return new Promise(function(resolve, reject) {
        api
          .PUBLISH(data)
          .then(res => {
            if (res.data.ok) {
              commit('OK', res.data.body)
              resolve(res)
            } else {
              commit('ER')
              reject(res)
            }
          })
          .catch(res => {
            commit('ER')
            reject(res)
          })
      })
    }
  }
})

export default store
