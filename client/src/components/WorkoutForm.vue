<template>
<div class="panel panel-default">
    <div class="panel-heading">
        <h2>Create Workout</h2></div>

    <div class="panel-body">
        <form class="form-horizontal">
            <div class="form-group row">
                <label class="col-sm-2 control-label" for="formGroupInputLarge">Date Proposed:</label>
                <div class="col-sm-3">
                    <input class="form-control" v-model="date_proposed" type="date" id="formGroupInputLarge">
                </div>
            </div>

            <exerciseForm :exercise="ex" v-for="ex in exercises"></exerciseForm>
            <div class="row">
                <div class="col-sm-4 col-sm-offset-4">
                    <div class="btn-group" role="group" aria-label="Buttons">
                        <button type="button" v-on:click="addRow" class="btn btn-secondary">Add Exercise</button>
                        <button type="submit" v-on:click="submitForm" class="btn btn-primary">Submit</button>
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
                reps: [0, 0, 0, 0, 0]
            })
        },

        submitForm: function(event) {
            event.preventDefault();

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
            console.log(data.exercises)

            this.$store.dispatch('addWorkout', data)
        }
    }
}
</script>
