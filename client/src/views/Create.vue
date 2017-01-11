<template>
<div>
  <div class="row">
    <div class="col-md-12">

      <div v-if="success" class="alert alert-success alert-dismissible" role="alert">
        <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <strong>Success!</strong> Workout saved
      </div>

      <div v-if="error" class="alert alert-danger alert-dismissible" role="alert">
        <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <strong>Error!</strong> Something went wrong. Try again!
      </div>

        <div class="well">
          <WorkoutForm @on:success="setSuccess" @on.failure="setFailure"></WorkoutForm>
        </div>
      </div>
  </div>
</div>
</template>


<script>
import WorkoutForm from '../components/WorkoutForm.vue'

export default {
  data: function () {
    return {
      success: false,
      error: false
    }
  },
  methods: {
    setSuccess: function () {
      this.success = true
    },
    setFailure: function () {
      this.error = true
    }
  },
  components: {
    WorkoutForm
  }
}
</script>
