import Vue from 'vue'
import Router from 'vue-router'
// import beforeEach from './beforeEach'

import Login from '../views/Login.vue'
import Dashboard from '../views/MainDashboard.vue'

Vue.use(Router)

const routes = [{
  name: 'catchall',
  path: '*',
  component: Login
}, {
  name: 'auth.login',
  path: '/login',
  component: Login
}, {
  name: 'dashboard',
  path: '/',
  component: Dashboard,
  meta: {
    requiresAuth: true
  }
}]

const router = new Router({
  mode: 'history',
  linkActiveClass: 'active',
  routes
})

// router.beforeEach(beforeEach)

export default router
