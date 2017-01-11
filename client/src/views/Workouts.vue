<template>
<div>
  <div class="row">
    <div class="col-md-12">
      <!-- TODO order by date proposed ascending -->
      <h2>Upcoming Workouts</h2>
      <div v-if="upcoming.length > 0" class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
        <workout v-for="(workout,index) in upcoming" :workout="workout"></workout>
      </div>
        <div v-else class="alert alert-info">
          <strong>Info!</strong> You've got no upcoming workouts bra!
        </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <h2>Past Workouts</h2>
      <!-- TODO order by date completed descending -->
      <div v-if="completed.length > 0" class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
        <workout v-for="(workout,index) in completed" :workout="workout"></workout>
      </div>
        <div v-else class="alert alert-info">
          <strong>Info!</strong> You've got no completed workouts bra! Get to the gym!
        </div>
    </div>
  </div>
</div>
</template>

<script>
import { mapGetters } from 'vuex'
import Workout from '../components/Workout.vue'

export default {
  components: {
    Workout
  },
  computed: {
    ...mapGetters(['upcoming', 'completed'])
  }
}
</script>
