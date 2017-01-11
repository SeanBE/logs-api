import Vue from 'vue'
import Vuex from 'vuex'

import auth from './modules/auth'
import workouts from './modules/workouts'
import exercises from './modules/exercises'

import {subscribe} from './plugins'
import createLogger from 'vuex/dist/logger.js'

Vue.use(Vuex)
Vue.config.debug = true
// const debug = process.env.NODE_ENV !== 'production'
const debug = true

export default new Vuex.Store({
  modules: {
    auth,
    workouts,
    exercises
  },
  // Only for development.
  strict: debug,
  plugins: debug ? [createLogger(), subscribe] : [subscribe]
})
