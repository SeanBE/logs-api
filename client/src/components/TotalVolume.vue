<template>
<div>
    <svg class="chart">
</svg>
</div>
</template>

<script>
import * as d3 from "d3";

let ages = [30, 22, 33, 45];

let chart = d3.select('.chart')

// 
// let bars = chart
//     .selectAll('g')
//     .data(ages)
//     .enter()
//     .append('hello')

// bars.append('rect')
//     .attr({
//         'x': function(d, i) {
//             return i * 10;
//         },
//         'width': 10 - 1,
//         'height': 10
//     })
</script>
