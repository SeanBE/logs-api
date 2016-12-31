import * as api from '../../api/'
import * as types from '../types'
import axios from 'axios'
import localforage from 'localforage'
import { userTokenStorageKey } from 'src/config'
import { isEmpty } from 'lodash'

const state = {
  token: null
}

const getters = {
  isLogged: ({ token }) => !isEmpty(token)
}

const actions = {
  NEW_TOKEN: ({ dispatch }, payload) => {
    api.newToken(payload)
      .then(({ data }) => {
        // TODO data not token? why??
        dispatch('SET_TOKEN', data.token)
        return
      })
  },
  SET_TOKEN: ({ commit }, payload) => {
    const token = (isEmpty(payload)) ? null : payload.token || payload
    commit(types.SET_TOKEN, token)
    return Promise.resolve(token)
  },
  CHECK_USER_TOKEN: ({ dispatch, state }) => {
    if (!isEmpty(state.token)) {
      return Promise.resolve(state.token)
    }
    return localforage.getItem(userTokenStorageKey)
      .then((token) => {
        if (isEmpty(token)) {
          return Promise.reject('NO_TOKEN')
        }
        return dispatch('SET_TOKEN', token) // keep promise chain
      })
  }
}

const mutations = {
  [types.SET_TOKEN] (state, token) {
    state.token = token
  }
}

const subscribe = (store) => {
  store.subscribe((mutation, { token }) => {
    if (types.SET_TOKEN === mutation.type) {
      axios.defaults.headers.common.Authorization = `Bearer ${token}`
      localforage.setItem(userTokenStorageKey, token)
    }
  })
}

export default {
  state,
  getters,
  actions,
  mutations,
  plugins: [subscribe]
}
