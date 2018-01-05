import Vue from 'vue'
import Router from 'vue-router'
import CrudForm from '@/pages/CrudForm'
import ArticleList from '@/pages/ArticleList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/list',
      name: 'ArticleList',
      component: ArticleList
    },
    {
      path: '/:action/:id',
      name: 'UpdateArticle',
      component: CrudForm
    },
    {
      path: '/:action',
      name: 'CreateArticle',
      component: CrudForm
    }
  ]
})
