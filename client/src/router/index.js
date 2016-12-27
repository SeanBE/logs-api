import Vue from 'vue'
import Router from 'vue-router'

import EditView from '../views/EditView.vue'
import DashboardView from '../views/Dashboard.vue'
import MainDashboardView from '../views/MainDashboard.vue'
import CreateView from '../views/Create.vue'
import WorkoutsView from '../views/Workouts.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [{
    name: 'notfound',
    path: '*',
    component: MainDashboardView
  }, {
    name: 'dashboard',
    path: '/',
    component: MainDashboardView
  }, {
    name: 'dashboard_alt',
    path: '/alt',
    component: DashboardView
  }, {
    name: 'create',
    path: '/create',
    component: CreateView
  }, {
    name: 'workouts',
    path: '/workouts',
    component: WorkoutsView
  }, {
    name: 'edit',
    path: '/edit/:id',
    component: EditView
  }]
})
