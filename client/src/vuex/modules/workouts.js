import api from '../../api/'
import * as types from '../types'

// state
const state = {
    workouts: []
}

//getters
const getters = {
    workouts: state => state.workouts
}

// actions
const actions = {
    addWorkout({
        commit
    }, workoutData) {
        api.addWorkout(workoutData,
            workout => {
                commit(types.ADD_WORKOUT_SUCCESS, {
                    workout
                })
            },
            error => {
                commit(types.ADD_WORKOUT_FAILURE)
            }
        )
    },
    getAllWorkouts({
        commit
    }) {
        // () => commit(types.CHECKOUT_FAILURE, { savedCartItems })
        api.getWorkouts(workouts => {
                commit(types.GET_WORKOUT_LIST_SUCCESS, {
                    workouts
                })
            },
            () => {
                commit(types.GET_WORKOUT_LIST_FAILURE)
            }
        )
    }
}

// mutations
const mutations = {
    [types.ADD_WORKOUT_SUCCESS](state, {
        workout
    }) {
        state.workouts.push(workout)
    },
    [types.ADD_WORKOUT_FAILURE](state) {},
    [types.GET_WORKOUT_LIST_SUCCESS](state, {
        workouts
    }) {
        state.workouts = workouts
    },
    [types.GET_WORKOUT_LIST_FAILURE](state) {
        state.workouts = []
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}
