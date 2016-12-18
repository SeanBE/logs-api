import Vue from 'vue'
import {
    sync
} from 'vuex-router-sync';

import router from './router/'
import store from './vuex/store'
import App from './views/App.vue'
import JQuery from 'jquery'
import BootstrapJs from 'bootstrap/dist/js/bootstrap'
import Bootstrap from 'bootstrap/dist/css/bootstrap.css';

sync(store, router)

new Vue({
    store,
    router,
    render: h => h(App),
}).$mount('#app')
