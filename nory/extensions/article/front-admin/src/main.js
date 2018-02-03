// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import helper from './js/helper'
global.helper = helper

import store from './store/'
global.store = store

import Vuetify from 'vuetify'
// import 'vuetify/dist/vuetify.css'

import App from './App'
import router from './router'
import i18n from './i18n/'

Vue.use(Vuetify)

import 'vuetify/src/stylus/main.styl'
// import 'vuetify/src/stylus/settings/_colors.styl'

// import Dropzone from 'vue2-dropzone'
// Vue.component('dropzone', Dropzone)

import VForm from './components/Form.vue'
import VGrid from './components/Grid.vue'
import VField from './components/Field.vue'

Vue.component('v-form', VForm)
Vue.component('v-grid', VGrid)
Vue.component('v-field', VField)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  i18n,
  router,
  store,
  template: '<App/>',
  components: { App }
})
