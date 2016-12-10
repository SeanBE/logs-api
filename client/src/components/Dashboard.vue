<template>
<div>
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
import {
    mapGetters
} from 'vuex'

export default {
    components: {
        Workout
    },
    computed: mapGetters({
        workouts: 'workouts'
    }),
    created() {
        this.$store.dispatch('getAllWorkouts')
    }
}
</script>
