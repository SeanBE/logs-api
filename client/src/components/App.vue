<template>
<div id="app" class="container">
    <nav class="navbar navbar-default">
        <div class="container-fluid">
            <div class="navbar-header">
                <router-link :to="{ name: 'dashboard' }">
                    <a class="navbar-brand">Sean Löfgren</a>
                </router-link>
            </div>

            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">

                <ul class="nav navbar-nav navbar-right">
                    <li>
                        <router-link :to="{ name: 'workouts' }"><a class="navbar-link">Dashboard</a></router-link>
                    </li>
                    <li>
                        <router-link :to="{ name: 'dashboard_alt' }"><a class="navbar-link">Calendar</a></router-link>
                    </li>
                    <li>
                        <router-link :to="{ name: 'workouts' }"><a class="navbar-link">Progress</a></router-link>
                    </li>
                    <li>
                        <router-link :to="{ name: 'workouts' }"><a class="navbar-link">Training Log</a></router-link>
                    </li>
                    <!-- TODO create workout will be removed later. -->
                    <li>
                        <router-link :to="{ name: 'create' }"><a class="navbar-link">Create</a></router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <router-view></router-view>
</div>
</template>
