import Vue from 'vue'
import Router from 'vue-router'

import routes from './routes'
import beforeEach from './beforeEach'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  linkActiveClass: 'active',
  routes
})

router.beforeEach(beforeEach)

export default router
