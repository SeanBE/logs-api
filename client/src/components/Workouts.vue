<template>
<div>
    <div class="row">
        <div class="col-md-12">
            <ul class="list-group">
                <li v-for="workout in workouts" class="list-group-item">

                    <button type="button" class="btn btn-info btn-sm" aria-label="Edit">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                    </button>
                    <button type="button" class="pull-right btn btn-danger btn-sm" aria-label="Delete">
                        <span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
                    </button>
                    Workout with {{Object.keys(workout.exercises).length}} exercises proposed on {{workout.date_proposed}} completed on {{workout.date_completed}}

                </li>
            </ul>
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
