<template>
<div class="panel panel-default">
  <div class="panel-heading">

      <div class="form-group" >
        <label class="control-label">Exercise:</label>
          <select class="form-control" v-model="exercise.name">
          <option v-for="option in exercises" v-bind:value="option.name">
            {{ option.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label class="control-label">Sets:</label>
        <select v-model.number="exercise.sets" class="form-control">
          <option v-for="n in 5">{{ n }}</option>
        </select>
      </div>

    </div>

  <div class="panel-body">
      <table class="table table-responsive">
        <thead>
          <th class="headers">Set</th>
          <th class="headers">Reps</th>
          <th class="headers">Weight</th>
          <th class="headers">Comment</th>
        </thead>

        <tbody>
          <tr v-for="n in exercise.sets">
            <td> {{n}} </td>
            <td><input type="number" v-model.number="exercise.reps[n-1]" class="form-control" /></td>
            <td><input type="number" v-model.number="exercise.weight[n-1]" class="form-control" /></td>
            <td><input type="text" v-model="exercise.comment[n-1]" class="form-control" /></td>
          </tr>
        </tbody>
      </table>

    </div>
</div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: ['exercise'],
  computed: {
    ...mapGetters(['exercises'])
  }
}
</script>

<style>
  .headers {
    text-align: center;
  }
</style>
