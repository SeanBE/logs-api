<template>
<div class="panel panel-default">
    <div class="panel-body">
        <form class="form-horizontal">
            <div class="form-group">
                <label class="col-sm-3 control-label">Date Proposed:</label>
                <div class="col-sm-2">
                    <input class="form-control" v-model="date_proposed" type="date">
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-3 control-label">Date Completed:</label>
                <div class="col-sm-2">
                    <input class="form-control" type="date">
                </div>
            </div>

            <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
                <exerciseForm :exercise="ex" :index="index" v-for="(ex, index) in exercises"></exerciseForm>
            </div>

            <div class="form-group">
                <div class="col-sm-4 col-sm-offset-4">
                    <div class="btn-group" role="group" aria-label="Buttons">
                        <button type="button" v-on:click="addRow" class="btn btn-secondary">Add Exercise</button>
                        <button type="submit" v-on:submit.prevent="onSubmit" class="btn btn-primary">Submit</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>
</template>


<script>
import ExerciseForm from './ExerciseForm.vue'

export default {
    data: function() {
        return {
            date_proposed: null,
            exercises: [{
                name: "",
                sets: 1,
                reps: [0, 0, 0, 0, 0]
            }]
        }
    },
    components: {
        ExerciseForm
    },
    methods: {
        addRow: function() {
            this.exercises.push({
                name: "",
                sets: 1,
                reps: [0, 0, 0, 0, 0]
            })
        },

        onSubmit: function(event) {

            // Validate form. Like set 2 cant be 0 and set3 can..
            // Add notification that it is submitted.

            let data = {}
            data.date_proposed = this.date_proposed
            data.exercises = this.exercises.reduce(function(merged, original) {
                merged[original.name] = []
                for (let r of original.reps) {
                    merged[original.name].push({
                        'reps': r,
                        'set_num': merged[original.name].length,
                        'comment': '',
                        'weight': 0
                    })
                }
                return merged
            }, {})

            this.$store.dispatch('addWorkout', data)
        }
    }
}
</script>
