<template>

    <form class="form-horizontal">
      <div class="form-group">
        <label class="col-sm-3 control-label">Date Proposed:</label>
        <div class="col-sm-3">
          <input class="form-control" v-model="date_proposed" type="date">
        </div>
      </div>
        <div class="form-group">
        <label class="col-sm-3 control-label">Workout Comment:</label>
        <div class="col-sm-9">
          <textarea class="form-control" placeholder="Workout Notes" v-model="comment" type="text">
        </div>
      </div>

      </div>

      <div class="panel-group">
        <exerciseForm :exercise="ex" :index="index" v-for="(ex, index) in exercises"></exerciseForm>
      </div>

      <div class="form-group">
        <div class="col-sm-4 col-sm-offset-4">
          <div class="btn-group" role="group" aria-label="Buttons">
            <button type="button" @click.prevent="addRow" class="btn btn-secondary">Add Exercise</button>
            <button type="submit" @click.prevent="onSubmit" class="btn btn-primary">Submit</button>
          </div>
        </div>
      </div>
    </form>

</template>

<script>
import ExerciseForm from './ExerciseForm.vue'

export default {
  data: function () {
    return {
      date_proposed: null,
      comment: '',
      // TODO this clean?
      // TODO update to new json rep.
      exercises: [{
        name: '',
        sets: 1,
        weight: [0, 0, 0, 0, 0],
        reps: [0, 0, 0, 0, 0],
        comment: ['', '', '', '', '']
      }]
    }
  },
  components: {
    ExerciseForm
  },
  props: ['success'],
  methods: {
    addRow: function () {
      // TODO update to new json rep.
      this.exercises.push({
        name: '',
        sets: 1,
        weight: [0, 0, 0, 0, 0],
        reps: [0, 0, 0, 0, 0],
        comment: ['', '', '', '', '']
      })
    },
    onSubmit: function () {
      // TODO Validation. No empty Exercise names.. etc.
      let workout = {date_proposed: this.date_proposed, comment: this.comment}

      // Prepare for post.
      workout.exercises = this.exercises.reduce(function (exercises, form) {
        let x = {'name': form.name, 'sets': []}
        for (let i = 0; i < form.sets; i++) {
          x['sets'].push({
            'reps': form.reps[i],
            'comment': form.comment[i],
            'weight': form.weight[i]
          })
        }
        exercises.push(x)
        return exercises
      }, [])
      console.log(workout)
      // TODO avoid multiple saves.
      // Send events to ParentView.
      var that = this
      this.$store.dispatch('ADD_WORKOUT', workout)
        .then(function (response) {
          that.$emit('success')
        }).catch(function (error) {
          console.log(error)
          that.$emit('failure')
        })
    }
  }
}
</script>
