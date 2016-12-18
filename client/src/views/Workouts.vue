<template>
<div>
    <div class="row">
        <div class="col-md-12">
            <ul class="list-group">
                <li v-for="workout in workouts" class="list-group-item">

                    <router-link :to="{ name: 'edit', params: {id: workout.uri} }">
                        <button type="button" class="btn btn-info btn-sm" aria-label="Edit">
                        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                      </button>
                    </router-link>
                    </router-link>
                    <button type="button" @click.prevent="deleteExercise(workout.uri)" class="pull-right btn btn-danger btn-sm" aria-label="Delete">
                        <span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
                    </button> Workout with {{Object.keys(workout.exercises).length}} exercises proposed on {{workout.date_proposed}} completed on {{workout.date_completed}} {{workout.uri}}
                </li>
            </ul>
        </div>
    </div>
</div>
</template>


<script>
import Workout from '../components/Workout.vue'
import {
    mapGetters
} from 'vuex'

export default {
    components: {
        Workout
    },
    methods: {
        deleteExercise: function(id) {
            console.log('deleting ', id)
            this.$store.dispatch('deleteWorkout', id)
        }
    },
    computed: mapGetters(['workouts']),
    created() {
        this.$store.dispatch('FETCH_WORKOUTS')
    }
}
</script>
