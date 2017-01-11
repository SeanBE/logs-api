<template>
<div class="well error-container">
      <h2>Oops! 404 Not Found</h2>
      <div>
        <router-link :to="{ name: 'dashboard' }">
          <a class="btn btn-primary btn-lg">
            <span class="glyphicon glyphicon-home"></span>
            Take Me Home </a>
            <!-- TODO return to previous link? -->
        </router-link>
      </div>
</div>
</template>

<style>
.error-container {
  text-align: center
}
</style>
