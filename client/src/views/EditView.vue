<template>
<div class="edit-view">
    <div class="row">
      <template v-if="workout">
        <h1>Workout : {{ workout.id }}</h1>
        <div class="col-md-12">
            <WorkoutForm></WorkoutForm>
        </div>
    </template>

    </div>
</div>
</template>


<script>
import WorkoutForm from '../components/WorkoutForm.vue'

function fetchWorkout(store) {
    return store.dispatch('FETCH_WORKOUT', {
        id: store.state.route.params.id
    })
}

export default {
    components: {
        WorkoutForm
    },
    computed: {
        workout () {
          // TODO this is not right.
            return this.$store.state.workouts.workouts[this.$route.params.id]
        }
    },
    beforeMount() {
        fetchWorkout(this.$store)
    }
}
</script>
