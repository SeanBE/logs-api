import Vue from 'vue'
import {
    sync
} from 'vuex-router-sync';

import router from './router'
import store from './vuex/store'
import App from './components/App.vue'

sync(store, router)

new Vue({
    store,
    router,
    render: h => h(App),
}).$mount('#app')
