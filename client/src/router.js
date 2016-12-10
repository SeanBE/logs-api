import Vue from 'vue'
import Router from 'vue-router';

import DashboardView from './components/Dashboard.vue'
import CreateView from './components/Create.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [{
        path: '/',
        component: DashboardView
    },{
        path: '/create',
        component: CreateView
    }]
})
