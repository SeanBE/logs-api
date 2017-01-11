<template>
<div>
  <h4>Comments</h4>
  <ul class="list-group">
    <li class="list-group-item"> Workout - {{comment}} </li>
    <li v-for="entry in filteredComments" class="list-group-item">{{entry.name}} - Set #{{entry.index}} : {{entry.comment}}</li>
  </ul>
</div>
</template>

<script>
export default {
  props: ['exercises', 'comment'],
  computed: {
    filteredComments: function () {
      return this.exercises.map(function (ex) {
        return ex['sets']
          .filter(set => set['comment'])
          .map((x, index) => Object.assign({}, x, {name: ex['name'], index: ex['sets'].indexOf(x) + 1}))
      }).reduce((a, b) => a.concat(b))
    }
  }
}
</script>
