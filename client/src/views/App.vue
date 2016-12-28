<template>
<div id="app" class="container">
    <nav class="navbar navbar-default">
        <div class="container-fluid">
            <div class="navbar-header">
                <router-link :to="{ name: 'login' }">
                    <a class="navbar-brand">Tracker</a>
                </router-link>
            </div>

            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">

                <ul class="nav navbar-nav navbar-right">
                    <li>
                        <router-link :to="{ name: 'dashboard' }"><a class="navbar-link">Private Link</a></router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <router-view></router-view>
</div>
</template>
