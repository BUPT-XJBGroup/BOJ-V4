import Vue from 'vue'
import Router from 'vue-router'
import Setting from '@/page/Setting'
import About from '@/page/About'
import Add from '@/page/Add'
import Markdown from '@/page/Markdown'
import Articles from '@/page/Articles'
import Login from '@/page/Login'
import Logout from '@/page/Logout'
import Article from '@/page/Article'
import Error from '@/page/Error'
import Edit from '@/page/Edit'
import Register from '@/page/Register'
import UpdateInfo from '@/page/UpdateInfo'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/markdown',
      name: 'Markdown',
      component: Markdown
    }, {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        NeedNotLogin: true
      }
    }, {
      path: '/setting',
      name: 'Setting',
      component: Setting,
      meta: {
        NeedLogin: true
      }
    }, {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/add',
      name: 'Add',
      component: Add,
      meta: {
        NeedStaff: true
      }
    },
    {
      path: '/articles',
      name: 'Articles',
      component: Articles
    },
    {
      path: '/',
      name: 'Markdown',
      component: Markdown
    },
    {
      path: '/article/:id',
      name: 'Article',
      component: Article
    },
    {
      path: '/error',
      name: 'Error',
      component: Error
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout
    },
    {
      path: '/edit/:id',
      name: 'Edit',
      component: Edit
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/updateInfo',
      name: 'UpdateInfo',
      component: UpdateInfo
    }
  ]
})
