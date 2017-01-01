import axios from 'axios'
import localforage from 'localforage'
import { userTokenStorageKey } from 'src/config'
import * as types from './types'

export const subscribe = (store) => {
  store.subscribe((mutation, data) => {
    if (types.SET_TOKEN === mutation.type) {
      // data must have auth + token.
      // TODO try {Auth} ?
      axios.defaults.headers.common.Authorization = `Bearer ${data.auth.token}`
      localforage.setItem(userTokenStorageKey, data.auth.token)
    }
  })
}
