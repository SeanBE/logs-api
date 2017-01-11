<template>
<div>
  <nav class="navbar navbar-default">
    <!-- TODO Two fluid containers? -->
    <div class="container-fluid">
      <div class="navbar-header">
        <router-link :to="{ name: 'dashboard' }">
          <a class="navbar-brand">Tracker</a>
        </router-link>
      </div>

      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">

        <ul v-show="isLogged" class="nav navbar-nav navbar-right">
          <li>
            <router-link :to="{ name: 'workouts' }"><a class="navbar-link">Workouts</a></router-link>
          </li>
          <li>
            <router-link :to="{ name: 'exercise.list' }"><a class="navbar-link">Exercises</a></router-link>
          </li>
          <li>
            <router-link :to="{ name: 'workout.new' }"><a class="navbar-link"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></a></router-link>
          </li>
          <li>
            <router-link :to="{ name: 'auth.logout' }"><a @click.prevent="logout" class="navbar-link"><span class="glyphicon glyphicon-log-out" aria-hidden="true"></span></a></router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</div>
</template>

<script>
import {
  mapGetters, mapActions
} from 'vuex'
export default {
  computed: {
    ...mapGetters(['isLogged'])
  },
  methods: {
    ...mapActions({'logout': 'REMOVE_TOKEN'})
  },
  watch: {
    isLogged (value) {
      if (value === false) {
        this.$router.push({
          name: 'auth.login'
        })
      }
    }
  }
}
</script>
