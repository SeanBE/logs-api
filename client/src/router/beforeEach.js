import store from '../vuex/store'

const beforeEach = (to, from, next) => {
  if (to.name !== 'auth.login' && to.name !== 'catchall') {
    store.dispatch('CHECK_USER_TOKEN')
      .then(() => {
        next()
      })
      .catch(() => {
        next({ name: 'auth.login' })
      })
  } else {
    next()
    return
  }
}

export default beforeEach
