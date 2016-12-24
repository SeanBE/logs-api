<template>
<div>
<h4>Comments</h4>
<ul class="list-group">
    <li v-for="entry in filteredComments" class="list-group-item">{{entry.exercise}} - Set #{{entry.set}} : {{entry.comment}}</li>
</ul>
</div>
</template>

<script>
export default {
    props: ['exercises'],
    computed: {
        filteredComments: function() {
            let comments = []

            for (let key of Object.keys(this.exercises)) {
                let c = this.exercises[key].map(function(set, index) {
                    if (set['comment']) {
                        return {
                            set: index,
                            exercise: key,
                            comment: set ['comment']
                        }
                    }
                }).filter(function(comment) {
                    return comment
                })
                comments.push(...c)
            }
            return comments;
        }
    }
}
</script>
