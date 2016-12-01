<template>
  <div class="panel panel-default">
        <div class="panel-heading" role="tab" :id="header">
            <h4 class="panel-title">
              <a role="button" data-toggle="collapse" data-parent="#accordion" :href="collapseHash" aria-expanded="true" :aria-controls="collapse">
                Workout {{workout.date_proposed}}
              </a>
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
                        <tr v-for="(sets,exercise) in workout.exercises">
                            <td>{{exercise}}</td>
                            <template v-for="set in sets">
<td>
    {{set.reps}}</td>
<td>{{set.weight}}</td>
</template>
                        </tr>
                      </tbody>
                      </table>
                      <comments :exercises="workout.exercises"></comments>
            </div>
        </div>
    </div>
</template>

<script>
import Comments from './Comments.vue'

export default {

    components : {
      Comments
    },
    props: ['workout', 'index'],
    computed: {
        header: function() {
            return `header${this.index}`
        },
        collapse: function() {
            return `collapse${this.index}`
        },
        collapseHash: function() {
            return `#collapse${this.index}`
        }
    }
}
</script>



<style></style>
