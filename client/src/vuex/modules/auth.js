import * as api from '../../api/'
import * as types from '../types'
import localforage from 'localforage'
import { userTokenStorageKey } from 'src/config'
import { isEmpty } from 'lodash'

const state = {
  token: null
}

const getters = {
  isLogged: ({ token }) => !isEmpty(token)
}

// dispatch for actions async commit sync .
const actions = {
  NEW_TOKEN: ({ dispatch }, payload) => {
    return api.newToken(payload)
      .then(({data}) => {
        dispatch('SET_TOKEN', data.token)
      })
  },
  SET_TOKEN: ({ commit }, token) => {
    commit(types.SET_TOKEN, token)
    return Promise.resolve(token)
  },
  REMOVE_TOKEN: ({ commit }) => {
    commit(types.REMOVE_TOKEN)
    localforage.removeItem(userTokenStorageKey)
  },
  CHECK_USER_TOKEN: ({ dispatch, state }) => {
    if (!isEmpty(state.token)) {
      return Promise.resolve(state.token)
    }
    return localforage.getItem(userTokenStorageKey)
      .then((token) => {
        if (isEmpty(token)) {
          return Promise.reject('No Token Found in Local Storage.')
        }
        return dispatch('SET_TOKEN', token)
      })
  }
}

const mutations = {
  [types.SET_TOKEN] (state, token) {
    state.token = token
  },
  [types.REMOVE_TOKEN] (state) {
    state.token = null
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
