<template>
<div>
  <div class="row">
    <div class="col-md-12">
      <div v-show="showError" class="alert alert-danger alert-dismissible" role="alert">
        <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <strong>Error!</strong> Yo Bro! You're password is all wrong and shit. Fix it son!
      </div>

      <form class="well" @submit.prevent="submit">
        <div class="form-group">
          <label for="username" class="control-label">Username</label>
          <input type="text" class="form-control" id="username" placeholder="Your username" v-model="username">
        </div>
        <div class="form-group">
          <label for="password" class="control-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="password">
        </div>
        <button class="btn btn-primary btn-block" type="submit">Sign In</button>
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
      username: '',
      password: '',
      showError: false
    }
  },
  methods: {
    ...mapActions(['NEW_TOKEN']),
    submit () {
      const { username, password } = this
      this.NEW_TOKEN({ username, password })
        .then(() => {
          this.$router.push({ name: 'dashboard' })
        }).catch(() => {
          this.showError = true
        })
    }
  }
}
</script>
