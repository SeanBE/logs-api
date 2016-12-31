import store from '../vuex/store'

const needAuth = auth => auth === true

const beforeEach = (to, from, next) => {
  const auth = to.meta.requiresAuth

  if (!needAuth(auth)) {
    next()
    return
  }

  store.dispatch('CHECK_USER_TOKEN')
    .then(() => {
      next()
    })
    .catch(() => {
      next({ name: 'auth.login' })
    })
}

export default beforeEach
