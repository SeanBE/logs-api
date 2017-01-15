import Login from '../views/Login.vue'
import NotFound from '../views/NotFound.vue'
import Workouts from '../views/Workouts.vue'
import Create from '../views/Create.vue'
import Edit from '../views/EditView.vue'
import Exercises from '../views/Exercises.vue'
import Home from '../views/Home.vue'
// import Graphs from '../views/Graphs.vue'

const routes = [
  { name: 'auth.login', path: '/login', component: Login },
  { name: 'auth.logout', path: '/logout', redirect: { name: 'auth.login' } },
  { name: 'dashboard', path: '/', component: Home },
  // { name: 'graphs', path: '/graphs', component: Graphs },
  { name: 'catchall', path: '*', component: NotFound },
  // Workouts
  { name: 'workouts', path: '/workouts', component: Workouts },
  { name: 'workout', path: '/workout/:id', component: Workouts },
  { name: 'workout.new', path: '/new', component: Create },
  { name: 'workout.edit', path: '/edit/:id', component: Edit },
  { name: 'workout.delete', path: '/delete/:id', component: Create },
  // Exercises
  { name: 'exercise.list', path: '/exercises', component: Exercises }
]

export default routes
