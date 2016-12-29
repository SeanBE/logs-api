<template>
<div id="app" class="container">
  <navBar></navBar>
  <router-view></router-view>
</div>
</template>

<script>
import NavBar from '../components/NavBar.vue'

export default {
  components: {
    NavBar
  }
}
</script>
