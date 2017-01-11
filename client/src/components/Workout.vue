<template>
<div class="panel panel-default">
  <div class="panel-heading" role="tab" :id="header">
      <h4 class="panel-title">

      <a role="button" data-toggle="collapse" data-parent="#accordion" :href="collapseHash" aria-expanded="true" :aria-controls="collapse">
        Workout {{workout.date_proposed}}
      </a>

      <div class="pull-right">
      <button type="button" @click.prevent="deleteExercise(workout)" class="btn btn-danger btn-xs" aria-label="Delete">
        <span class="glyphicon glyphicon-trash" aria-hidden="true"></span>
      </button>
      <button @click="goToEdit(workout)" type="button" class="btn btn-info btn-xs" aria-label="Edit">
        <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
      </button>
      </div>
    </h4>
  </div>
  <div :id="collapse" class="panel-collapse collapse in" role="tabpanel" :aria-labelledby="header">
    <div class="panel-body">
      <table class="table table-striped">
        <thead>
          <template v-for="n in 5">
            <th colspan="2" style="text-align:right;">Set #{{n}}</th>
          </template>
        </thead>
        <thead>
          <th> Exercise </th>
            <template v-for="n in 5">
              <th> Reps</th>
              <th> Weight </th>
            </template>
        </thead>
          <tbody>
          <tr v-for="exercise in workout.exercises">
                <td>{{exercise.name}}</td>
                <template v-for="set in exercise.sets">
                    <td>
                    {{set.reps}}</td>
                    <td>{{set.weight}}</td>
                  </template>
            </tr>
          </tbody>
          </table>
          <comments :comment="workout.comment" :exercises="workout.exercises"></comments>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import Comments from './Comments.vue'

export default {
  components: {
    Comments
  },
  methods: {
    ...mapActions({deleteExercise: 'DELETE_WORKOUT'}),
    goToEdit (workout) {
      this.$store.commit({type: 'SET_ACTIVE_WORKOUT', workout: workout})
      this.$router.push({name: 'workout.edit', params: { id: workout.id }})
    }
  },
  props: ['workout'],
  computed: {
    // TODO change this to v-bind:... get rid of dis shit.
    header: function () {
      return `header${this.workout.id}`
    },
    collapse: function () {
      return `collapse${this.workout.id}`
    },
    collapseHash: function () {
      return `#collapse${this.workout.id}`
    }
  }
}
</script>
<style></style>
