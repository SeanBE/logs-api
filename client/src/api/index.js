// import Vue from 'vue'
import axios from 'axios'

// TODO ???
export const API_ROOT = (process.env.NODE_ENV === 'production')
  ? 'http://localhost:5000/api/1/'
  : 'http://localhost:5000/api/1/'

axios.defaults.baseURL = API_ROOT

export default {
  getWorkouts (callback) {
    axios.get('workouts/', {
      auth: {
        username: 'sean',
        password: 'test'
      }
    }).then(response => {
      callback(response.data)
    }).catch(error => {
      console.log(error)
    })
  },
  addWorkout (data, callback) {
    axios.post('workouts/', data).then(response => {
      callback(response.data)
    }).catch(error => {
      console.log(error)
    })
  },
  // TODO what is nicer. two callbacks or one callback with two return values??
  getWorkout (id, callback) {
    axios.get('workouts/' + id, {
      auth: {
        username: 'sean',
        password: 'test'
      }
    }).then(response => {
      console.log(response.data)
      callback(response.data)
    }).catch(error => {
      console.log(error)
    })
  },
  deleteWorkout (id, callback) {
    axios.delete('workouts/' + id, {
      auth: {
        username: 'sean',
        password: 'test'
      }
    }).then(response => {
      console.log(response)
      callback(response)
    }).catch(error => {
      console.log(error)
    })
  }
}
