<template>
<div>
  <div class="row">
    <div class="col-md-12">
      <h2>Exercises</h2>

      <div class="form-group well">
        <div class="input-group">
          <input type="text" v-model="searchQuery" class="form-control input-lg" placeholder="Search">
          <div class="input-group-addon"><i class="glyphicon glyphicon-search"></i></div>
        </div>
      </div>

      <button v-if="showCreate" @click.prevent="createExercise" class="btn btn-info center-block" type="button">
        Create Exercise
      </button>

      <ul v-if="filtered.length > 0" class="list-group well">
        <a v-for="exercise in filtered" class="list-group-item">
          <h4 class="list-group-item-heading">{{exercise.name}}</h4>
          <p class="list-group-item-text">{{exercise.comment}}</p>
        </a>
      </ul>

      <h4>Recently Used</h4>
      <ul class="list-group well">
        <a href="#" v-for="exercise in recentlyUsed" class="list-group-item">
          <h4 class="list-group-item-heading">{{exercise.name}}</h4>
          <p class="list-group-item-text">{{exercise.comment}}</p>
        </a>
      </ul>

    </div>
  </div>
</div>

</div>
</template>


<script>
import { isEmpty } from 'lodash'
import {
  mapGetters
} from 'vuex'

export default {
  data: function () {
    return {
      searchQuery: '',
      showCreate: false
    }
  },
  methods: {
    createExercise: function () {
      this.$store.dispatch('ADD_EXERCISE', {
        'name': this.searchQuery
      }).then(() => console.log('success. replace with event emit.'))
        .catch((error) => console.log(error))
    }
  },
  computed: {
    ...mapGetters(['recentlyUsed', 'exercises']),
    filtered: function () {
      if (!this.searchQuery) {
        return []
      }
      let searchQuery = this.searchQuery.trim().toLowerCase()
      let filtered = this.exercises.filter(function (ex) {
        if (ex.name.toLowerCase().indexOf(searchQuery) !== -1) {
          return ex
        }
      })

      if (isEmpty(filtered)) {
        this.showCreate = true
        return []
      }
      return filtered
    }
  }
}
</script>
