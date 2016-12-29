import Vue from 'vue'
import * as api from '../../api/'
import * as types from '../types'

const state = {
  workouts: { /* [id: number]: Workout */ }
}

const getters = {
  workouts: state => state.workouts
}

const actions = {
  FETCH_WORKOUTS: ({ commit, state }) => {
    api.getWorkouts(
      workouts => commit(types.SET_WORKOUTS, workouts)
    )
  },
  FETCH_WORKOUT: ({ commit, state }, { id }) => {
    return state.workouts[id]
  },

  addWorkout ({ commit }, workoutData) {
    api.addWorkout(workoutData,
      workout => commit(types.ADD_WORKOUT_SUCCESS, { workout })
    )
  },
  deleteWorkout ({ commit }, id) {
    api.deleteWorkout(id,
      () => commit(types.REMOVE_WORKOUT_SUCCESS, id)
    )
  }
}

const mutations = {
  [types.SET_WORKOUTS] (state, workouts) {
    workouts.forEach(workout => {
      if (workout) {
        Vue.set(state.workouts, workout.id, workout)
      }
    })
  },

  [types.ADD_WORKOUT_SUCCESS] (state, { workout }) {
    state.workouts.push(workout)
  },

  [types.REMOVE_WORKOUT_SUCCESS] (state, id) {
    for (var i = state.workouts.length - 1; i--;) {
      if (state.workouts[i].id === id) state.workouts.splice(i, 1)
    }
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
