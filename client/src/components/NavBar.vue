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

        <ul class="nav navbar-nav navbar-left">
          <li>
            <router-link v-show="!isLogged" :to="{ name: 'auth.login' }"><a class="navbar-link">Login</a></router-link>
          </li>
        </ul>

        <ul class="nav navbar-nav navbar-right">
          <li>
            <router-link v-show="isLogged" :to="{ name: 'workouts' }"><a class="navbar-link">Workouts</a></router-link>
          </li>
          <li>
            <router-link v-show="isLogged" :to="{ name: 'workout.new' }"><a class="navbar-link">Create</a></router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</div>
</template>

<script>
import {
  mapGetters
} from 'vuex'
export default {
  computed: {
    ...mapGetters(['isLogged'])
  },
  created: function () {
    // TODO nasty flicker of login.
    this.$store.dispatch('CHECK_USER_TOKEN')
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
