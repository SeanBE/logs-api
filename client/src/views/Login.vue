<template>
<div>
  <div class="row">
    <div class="col-md-12">

      <form class="well" @submit.prevent="submit">
        <div class="form-group">
          <label for="username" class="control-label">Username</label>
          <input type="text" class="form-control" id="username" v-model="username">
        </div>
        <div class="form-group">
          <label for="password" class="control-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="password">
        </div>
        <button class="btn btn-primary btn-block" type="submit">Login</button>
        <el-button>Default Button</el-button>

      </form>

    </div>
  </div>
</div>
</template>

<script>
import {
  mapActions
} from 'vuex'

export default {
  data () {
    return {
      username: 'example',
      password: '123456'
    }
  },
  methods: {
    ...mapActions(['NEW_TOKEN']),

    submit () {
      const { username, password } = this

      this.NEW_TOKEN({ username, password })
        .then(() => {
          this.$router.push({ name: 'dashboard' })
        })
    }
  }
}
</script>
