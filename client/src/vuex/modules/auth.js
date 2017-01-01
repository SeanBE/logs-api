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

const actions = {
  NEW_TOKEN: ({ dispatch }, payload) => {
    api.newToken(payload)
      .then(response => {
        // TODO fix case of no response
        dispatch('SET_TOKEN', response.data.token)
      })
  },
  SET_TOKEN: ({ commit }, token) => {
    // Takes in token as param.
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

export default {
  state,
  getters,
  actions,
  mutations
}
