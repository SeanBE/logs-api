<template>
  <div class="row">
    <div class="col-md-12">
      <h1>Edit Workout        <button type="button" @click.prevent="updateWorkout" class="btn btn-primary">Update</button></h1>

        <label class="control-label">Date Proposed:</label>
          <input class="form-control" :value="workout.date_proposed" @input="updateDetails" name="date_proposed" type="date">
        <label class="control-label">Date Completed:</label>
          <input class="form-control" :value="workout.date_completed" @input="updateDetails" name="date_completed" type="date">
          <label class="control-label">Workout comments:</label>
          <input class="form-control" :value="workout.comment" @input="updateDetails" name="comment" type="text">

        <div v-for="(exercise, exIndex) in workout.exercises">
        <h4>{{exercise.name}}</h4>
        <table class="table table-bordered">
          <tbody>
            <tr v-for="(set, setIndex) in exercise.sets">
              <td><input type="number" :value="set.reps"
                  @input="updateSets(exIndex, setIndex, 'reps', $event)" class="form-control" /></td>
              <td><input type="number" :value="set.weight"
                  @input="updateSets(exIndex, setIndex, 'weight', $event)" class="form-control" /></td>
              <td><input type="text" :value="set.comment"
                  @input="updateSets(exIndex, setIndex, 'comment', $event)" class="form-control" /></td>
            </tr>
          </tbody>
        </table>

        <!-- TODO differnce between click and submit.prevent -->
      <!-- TODO. Allow editing exercise names, number of sets. -->
        <!-- <select v-model="exercise" class="form-control">
            <option v-for="exercise in exercises">{{exercise.name}}</option>
        </select>
        <button type="button" @click.prevent="addExercise({workout:workout, exercise:exercise})" class="btn">Add Exercise</button> -->
        <!-- <th><button type="button" @click.prevent="addSet({workout:workout, exercise:exercise})" class="btn">Add Set</button></th> -->

    </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      workout ({workouts}) {
        // TODO Why not arrow function?
        return workouts.workout
      }
    })
  },
  methods: {
    updateDetails: function (e) {
      this.$store.dispatch('CHANGE_WORKOUT_DETAILS', {attr: e.target.name, value: e.target.value})
    },
    updateSets: function (exIndex, setIndex, attribute, e) {
      this.$store.dispatch('CHANGE_EXERCISES', {
        exercise: exIndex,
        set: setIndex,
        attr: attribute,
        value: e.target.value})
    },
    updateWorkout () {
      // TODO Validation.
      this.$store.dispatch('UPDATE_WORKOUT')
    }
  }
}

</script>
