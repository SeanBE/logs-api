import Vue from 'vue'
import Router from 'vue-router'
import beforeEach from './beforeEach'

import Login from '../views/Login.vue'
import Workouts from '../views/Dashboard.vue'
import Create from '../views/Create.vue'
import Dashboard from '../views/MainDashboard.vue'

Vue.use(Router)
const routes = [
  {name: 'catchall', path: '*', component: Dashboard, meta: { requiresAuth: false }},
  {name: 'auth.login', path: '/login', component: Login, meta: { requiresAuth: false }},
  {name: 'dashboard', path: '/', component: Dashboard, meta: { requiresAuth: false }},
  {name: 'workouts', path: '/workouts', component: Workouts, meta: { requiresAuth: true }},
  {name: 'workout', path: '/workout/:id', component: Workouts, meta: { requiresAuth: true }},
  {name: 'workout.new', path: '/new', component: Create, meta: { requiresAuth: true }},
  {name: 'workout.edit', path: '/edit/:id', component: Create, meta: { requiresAuth: true }},
  {name: 'workout.delete', path: '/delete/:id', component: Create, meta: { requiresAuth: true }}
]

const router = new Router({
  mode: 'history',
  linkActiveClass: 'active',
  routes
})

router.beforeEach(beforeEach)

export default router
