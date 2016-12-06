<template >
<div id="exerciseForm">
    <hr>
    <div class="form-group">
        <div class="row">
            <label class="col-sm-2 control-label" for="0">Exercise:</label>
            <div class="col-sm-2">
                <input type="text" v-model="exercise.name" class="form-control" id="0" placeholder="Exercise">
            </div>
            <label class="col-sm-2 control-label">Reps:</label>
            <div class="col-sm-1">
                <input type="number" v-model.number="exercise.reps[0]" class="form-control" placeholder="#1">
            </div>
            <div class="col-sm-1">
                <input type="number" v-model.number="exercise.reps[1]" class="form-control" placeholder="#2">
            </div>
            <div class="col-sm-1">
                <input type="number" v-model.number="exercise.reps[2]" class="form-control" placeholder="#3">
            </div>
            <div class="col-sm-1">
                <input type="number" v-model.number="exercise.reps[3]" class="form-control" placeholder="#4">
            </div>
            <div class="col-sm-1">
                <input type="number" v-model.number="exercise.reps[4]" class="form-control" placeholder="#5">
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: ['exercise'],
    methods: {
        updateValue: function() {
            this.$emit('changed-value')
        }
    }
}
</script>
