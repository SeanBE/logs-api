import Vue from 'vue'
import Vuex from 'vuex'

import {subscribe} from './plugins'
import auth from './modules/auth'
import workouts from './modules/workouts'
import createLogger from 'vuex/dist/logger.js'

Vue.use(Vuex)
Vue.config.debug = true
// const debug = process.env.NODE_ENV !== 'production'
const debug = true

export default new Vuex.Store({
  modules: {
    auth,
    workouts
  },
  strict: debug,
  plugins: debug ? [createLogger(), subscribe] : [subscribe]
})
