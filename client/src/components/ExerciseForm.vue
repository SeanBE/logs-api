<template>
<div class="panel panel-default">
  <div class="panel-heading" role="tab" :id="header">
    <div class="row">
      <label class="col-sm-2 control-label">Exercise:</label>
      <div class="col-sm-2">
        <input type="text" v-model="exercise.name" class="form-control" placeholder="Exercise">
      </div>
      <label class="col-sm-2 control-label">Sets:</label>
      <div class="col-sm-2">
        <select v-model.number="exercise.sets" class="form-control">
                  <option v-for="n in 5">
                    {{ n }}
                  </option>
                </select>
      </div>

      <a role="button" data-toggle="collapse" data-parent="#accordion" :href="collapseHash" aria-expanded="true" :aria-controls="collapse">
        <button type="button" class="btn btn-default" aria-label="Left Align">
              <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
              <!--  TODO if loop for icon.-->
            </button>
      </a>
    </div>

  </div>
  <div :id="collapse" class="panel-collapse collapse in" role="tabpanel" :aria-labelledby="header">
    <div class="panel-body">
      <div class="row" v-for="n in exercise.sets">

        <label class="col-xs-2 control-label">Set #{{n}} Reps:</label>
        <div class="col-xs-1">
          <input type="number" v-model.number="exercise.reps[n-1]" class="form-control">
        </div>

        <label class="col-xs-2 control-label">Weight:</label>
        <div class="col-xs-1">
          <input type="number" class="form-control">
        </div>

        <label class="col-xs-2 control-label">Tempo:</label>
        <div class="col-xs-1">
          <input type="number" class="form-control">
        </div>

      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: ['exercise', 'index'],
  computed: {
    header: function () {
      return `header${this.index}`
    },
    collapse: function () {
      return `collapse${this.index}`
    },
    collapseHash: function () {
      return `#collapse${this.index}`
    }
  }
}
</script>
