import * as api from '../../api/'
import * as types from '../types'

const state = {
  exercises: []
}

const getters = {
  exercises: state => state.exercises,
  recentlyUsed: state => state.exercises
}

const actions = {
  FETCH_EXERCISES: ({ commit, state }) => {
    return api.getExercises()
      .then(({ data }) => commit(types.SET_EXERCISES, data))
      .catch(error => console.error('Error get exercises api:', error))
  },
  ADD_EXERCISE: ({ commit }, data) => {
    return api.addExercise(data)
      .then(({data}) => commit(types.ADD_EXERCISE, data)
    )
  }
}

const mutations = {
  [types.ADD_EXERCISE] (state, exercise) {
    state.exercises.push(exercise)
  },
  [types.SET_EXERCISES] (state, exercises) {
    state.exercises = exercises
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
