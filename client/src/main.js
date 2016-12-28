import Vue from 'vue'
import {
    sync
} from 'vuex-router-sync'

import router from './router/'
import store from './vuex/store'
import App from './views/App.vue'
import 'jquery'
import 'bootstrap/dist/js/bootstrap'
import 'bootstrap/dist/css/bootstrap.css'

sync(store, router)

/* eslint-disable no-new */
new Vue({
  store,
  router,
  el: '#app',
  render: h => h(App)
})
