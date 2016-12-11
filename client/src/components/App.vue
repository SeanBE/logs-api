<template>
<div id="app" class="container">
    <nav class="navbar navbar-default">
        <div class="container-fluid">
            <div class="navbar-header">
                <router-link :to="{ name: 'dashboard' }">
                    <a class="navbar-brand">Training Tracker</a>
                </router-link>
            </div>

            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav">
                    <li><router-link :to="{ name: 'workouts' }"><a class="navbar-link">Workouts</a></router-link></li>
                </ul>

                <ul class="nav navbar-nav navbar-right">
                    <li>
                        <router-link :to="{ name: 'create' }"><a class="navbar-link">Create Workout</a></router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <router-view></router-view>
</div>
</template>
