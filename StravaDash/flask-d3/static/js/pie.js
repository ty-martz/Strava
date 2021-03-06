var margin = 20;
var width = 360;
var height = 360;
var radius = Math.min(width, height) / 2 - margin;

var svg = d3.select("#pie2")
    .append("svg")
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var graphData = {{ data | safe }}
//console.log(graphData)

// set the color scale
var color = d3.scaleOrdinal()
    .domain(graphData)
    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56"])

// Compute the position of each group on the pie:
var pie = d3.pie()
    .value(function(d) {return d.value; })
var data_ready = pie(d3.entries(graphData))

// Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
svg.selectAll('whatever')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d', d3.arc()
        .innerRadius(0)
        .outerRadius(radius)
    )
    .attr('fill', function(d){ return(color(d.value)) })
    .attr("stroke", "black")
    .style("stroke-width", "2px")
    .style("opacity", 0.7)

    var arcGenerator = d3.arc()
        .innerRadius(0)
        .outerRadius(radius)

svg.selectAll('mySlices')
    .data(data_ready)
    .enter()
    .append('text')
    .text(function(d){ return d.data.key})
    .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
    .style("text-anchor", "middle")
    .style("font-size", 17)