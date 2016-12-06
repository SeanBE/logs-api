// import Vue from 'vue'
import axios from 'axios'

export const API_ROOT = (process.env.NODE_ENV === 'production') ?
    'http://localhost:5000/api/1/' :
    'http://localhost:5000/api/1/'

axios.defaults.baseURL = API_ROOT

export default {
    getWorkouts(callback, errorCallback) {
        axios.get('workouts/').then(response => {
            callback(response.data)
        }).catch(error => {
            errorCallback(error)
        })
    },
    addWorkout(data, callback, errorCallback) {
        axios.post('workouts/', data).then(response => {
            callback(response.data)
        }).catch(error => {
            errorCallback(error)
        })
    }
}
