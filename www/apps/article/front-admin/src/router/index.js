import Vue from 'vue'
import Router from 'vue-router'
import CrudForm from '@/pages/CrudForm'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'CrudForm',
      component: CrudForm
    }
  ]
})
