<template>
<div id="app" class="container">
    <h1> Strength Admin</h1>
    <div class="row">
        <div class="col-md-12">
            <WorkoutForm></WorkoutForm>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
                <workout v-for="(workout,index) in workouts" :workout="workout" :index="index"></workout>
            </div>
        </div>
    </div>

</div>
</template>


<script>
import Workout from './Workout.vue'
import WorkoutForm from './WorkoutForm.vue'
import {
    mapGetters
} from 'vuex'


export default {
    components: {
        Workout,
        WorkoutForm
    },
    computed: mapGetters({
        workouts: 'workouts'
    }),
    created() {
        this.$store.dispatch('getAllWorkouts')
    }
}
</script>

<style>

</style>
