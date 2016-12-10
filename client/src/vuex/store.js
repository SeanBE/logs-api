import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'
import * as getters from './getters'
import workouts from './modules/workouts'
import createLogger from 'vuex/dist/logger.js'

Vue.use(Vuex)
Vue.config.debug = true

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  actions,
  getters,
  modules: {
    workouts
  },
  strict: debug,
  plugins: debug ? [createLogger()] : []
})
