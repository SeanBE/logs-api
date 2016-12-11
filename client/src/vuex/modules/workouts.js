import api from '../../api/'
import * as types from '../types'

const state = {
    workouts: []
}

const getters = {
    workouts: state => state.workouts
}

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
    deleteWorkout({
        commit
    }, id) {
        api.deleteWorkout(id,
            () => {
                commit(types.REMOVE_WORKOUT_SUCCESS, id)
            })
    },
    getAllWorkouts({
        commit
    }) {
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

const mutations = {
    [types.ADD_WORKOUT_SUCCESS](state, {
        workout
    }) {
        state.workouts.push(workout)
    },
    [types.ADD_WORKOUT_FAILURE](state) {},
    [types.REMOVE_WORKOUT_SUCCESS](state, id) {
        for (var i = state.workouts.length - 1; i--;) {
            if (state.workouts[i].uri === id) state.workouts.splice(i, 1)
        }
    },
    // [types.REMOVE_WORKOUT_FAILURE](state) {},
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
