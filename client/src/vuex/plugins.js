import axios from 'axios'
import localforage from 'localforage'
import { userTokenStorageKey } from 'src/config'
import * as types from './types'

export const subscribe = (store) => {
  store.subscribe((mutation, {auth}) => {
    if (types.SET_TOKEN === mutation.type) {
      axios.defaults.headers.common.Authorization = `Bearer ${auth.token}`
      localforage.setItem(userTokenStorageKey, auth.token)
    }
  })
}
