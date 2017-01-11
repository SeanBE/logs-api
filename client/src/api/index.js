import axios from 'axios'

export const API_ROOT = (process.env.NODE_ENV === 'production')
  ? 'http://104.236.219.109/api/1/'
  : 'http://localhost:8001/1/'

axios.defaults.baseURL = API_ROOT

// WORKOUT
export const getWorkouts = () => {
  return axios.get('workouts/')
}

export const addWorkout = (data) => {
  return axios.post('workouts/', data)
}

export const deleteWorkout = (id) => {
  return axios.delete('workouts/' + id)
}

export const updateWorkout = (id, data) => {
  return axios.patch('workouts/' + id, data)
}

// AUTH
export const newToken = ({ username, password }) => {
  return axios.post('tokens/', {}, {
    auth: {
      username: username,
      password: password
    }
  })
}

export const removeToken = () => {
  return axios.delete('tokens/')
}

// EXERCISE
export const addExercise = (data) => {
  return axios.post('exercises/', data)
}

export const getExercises = () => {
  return axios.get('exercises/')
}
