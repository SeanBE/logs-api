// import Vue from 'vue'
import axios from 'axios'

export const API_ROOT = (process.env.NODE_ENV === 'production') ?
    'http://localhost:5000/api/1/' :
    'http://localhost:5000/api/1/'

axios.defaults.baseURL = API_ROOT

export default {
    getWorkouts(callback, errorCallback) {
        axios.get('workouts/', {
            auth: {
                username: 'user',
                password: 'password'
            }
        }).then(response => {
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
    },
    deleteWorkout(id, callback) {
        axios.delete('workouts/' + id, {
            auth: {
                username: 'user',
                password: 'password'
            }
        }).then(response => {
            console.log(response)
            callback(response)
        }).catch(error => {
            console.log(error)
        })
    }
}
