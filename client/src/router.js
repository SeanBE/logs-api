import Vue from 'vue'
import Router from 'vue-router';

import DashboardView from './components/Dashboard.vue'
import CreateView from './components/Create.vue'
import WorkoutsView from './components/Workouts.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [{
        name: 'dashboard',
        path: '/',
        component: DashboardView
    },{
        name: 'create',
        path: '/create',
        component: CreateView
    },{
        name: 'workouts',
        path: '/workouts',
        component: WorkoutsView
    }]
})
