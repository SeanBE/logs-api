import axios from 'axios'

// export const API_ROOT = (process.env.NODE_ENV === 'production')
//   ? 'http://localhost/api/1/'
//   : 'http://localhost/api/1/'

axios.defaults.baseURL = process.env.API_ROOT

export const getWorkouts = (callback) => {
  axios.get('workouts/').then(response => {
    callback(response.data)
  })
}

export const addWorkout = (data, callback) => {
  axios.post('workouts/', data)
    .then(response => {
      callback(response.data)
    })
}

export const getWorkout = (id, callback) => {
  axios.get('workouts/' + id)
    .then(response => {
      callback(response.data)
    })
}

export const deleteWorkout = (id, callback) => {
  axios.delete('workouts/' + id)
    .then(response => {
      callback(response)
    })
}

export const newToken = ({ username, password }) => {
  return axios.post('tokens/', {}, {
    auth: {
      username: username,
      password: password
    }
  })
}
