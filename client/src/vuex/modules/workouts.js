import Vue from 'vue'
import { isEmpty } from 'lodash'
import * as api from '../../api/'
import * as types from '../types'

const state = {
  workouts: [],
  workout: { /* Workout currently editing.. */ }
}

// arr.$set(index, value) which is just syntax sugar for arr.splice(index, 1, value)

const getters = {
  workout: state => state.workout,
  workouts: state => state.workouts,
  upcoming: state => {
    return state.workouts.filter(function (workout) {
      return isEmpty(workout.date_completed)
    })
  },
  completed: state => {
    return state.workouts.filter(function (workout) {
      return !isEmpty(workout.date_completed)
    })
  }
}

const actions = {
  FETCH_WORKOUTS: ({ commit, state }) => {
    api.getWorkouts()
      .then(({data}) => commit(types.SET_WORKOUTS, data))
  },
  DELETE_WORKOUT: ({ commit }, workout) => {
    api.deleteWorkout(workout.id)
    .then(() => commit(types.REMOVE_WORKOUT, workout))
    .catch(error => console.log(error))
  },
  ADD_WORKOUT: ({ commit }, workout) => {
    return api.addWorkout(workout)
    .then(({data}) => commit(types.ADD_WORKOUT, data))
  },
  CHANGE_WORKOUT_DETAILS: ({ commit }, payload) => {
    commit(types.CHANGE_WORKOUT_DETAILS, payload)
  },
  CHANGE_EXERCISES: ({ commit }, payload) => {
    commit(types.CHANGE_EXERCISES, payload)
  },
  UPDATE_WORKOUT: ({ commit, state }) => {
    return api.updateWorkout(state.workout.id, state.workout)
    .then(() => commit(types.CLEAR_ACTIVE_WORKOUT))
  }
}

const mutations = {
  [types.SET_WORKOUTS] (state, workouts) {
    state.workouts = workouts
  },
  [types.ADD_WORKOUT] (state, workout) {
    state.workouts.push(workout)
  },
  [types.REMOVE_WORKOUT] (state, workout) {
    state.workouts.splice(state.workouts.indexOf(workout), 1)
  },
  [types.SET_ACTIVE_WORKOUT] (state, {workout}) {
    state.workout = workout
  },
  [types.CLEAR_ACTIVE_WORKOUT] (state) {
    state.workout = {}
  },
  [types.CHANGE_WORKOUT_DETAILS] (state, {attr, value}) {
    state.workout[attr] = value
  },
  [types.CHANGE_EXERCISES] (state, {exercise, set, attr, value}) {
    state.workout.exercises[exercise]['sets'][set][attr] = value
  },
  [types.ADD_SET_TO_WORKOUT] (state, {workout, exercise}) {
    state.workouts[state.workouts.indexOf(workout)].exercises[exercise]
        .push({'comment': '', 'set_num': 10, 'reps': 0, 'weight': 0})
  },
  [types.ADD_EXERCISE_TO_WORKOUT] (state, {workout, exercise}) {
    Vue.set(state.workouts[state.workouts.indexOf(workout)].exercises,
      exercise, [{'comment': '', 'set_num': 0, 'reps': 0, 'weight': 0}])
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
