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
      },
      list: []
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
    },
    ON_GET_ARTICLES(state, data) {
      state.article.list = data
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
    },
    UN_PUBLISH({ commit }, data) {
      return new Promise(function(resolve, reject) {
        api
          .UN_PUBLISH(data)
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
    ENABLE({ commit }, id) {
      return new Promise(function(resolve, reject) {
        api
          .PUBLISH(id)
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
    DISABLE({ commit }, id) {
      return new Promise(function(resolve, reject) {
        api
          .PUBLISH(id)
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
    GET_ARTICLES({ commit }) {
      return new Promise(function(resolve, reject) {
        api
          .GET_ARTICLES()
          .then(res => {
            if (res.data.ok) {
              commit('ON_GET_ARTICLES', res.data.body)
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
    GET_ARTICLE({ commit }, id) {
      return new Promise(function(resolve, reject) {
        api
          .GET_ARTICLE(id)
          .then(res => {
            if (res.data.ok) {
              commit('SAVE', res.data.body)
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
