
//set margin and sizes
var margin = {top:10, bottom:50, right:30, left:30};
var w = 800 - margin.left - margin.right;
var h = 800 - margin.top - margin.bottom;

//append svg
var svg = d3.select('#activity_bar')
    .append('svg')
    .attr('width', w - margin.left - margin.right)
    .attr('height', h - margin.top - margin.bottom)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

//parse data with chart building within
//d3.json('StravaDash/aggData/active_cnt.json', function(data) {
d3.csv('active_cnt.csv', function(data) {

    console.log(data)
    console.log(24)

    //Add axes
    var x = d3.scaleBand()
        .range([0, w])
        .domain(data.map(function(d) { return d.activity_type; }))
        .padding(0.2);
    
    svg.append('g')
        .attr('id', 'x-ax')
        .attr("transform", "translate(0," + h/1.37 + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");
    
    var y = d3.scaleLinear()
        .domain([0, 400])
        .range([ h-200, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // Add Bars
    svg.selectAll('active_bars')
        .data(data)
        .enter()
        .append("rect")
            .attr("x", function(d) { return x(d.activity_type); })
            .attr("width", x.bandwidth())
            .attr("fill", "#69b3a2")
            // no bar at the beginning thus:
            .attr("height", function(d) { return h - y(0); }) // always equal to 0
            .attr("y", function(d) { return y(0); })

    // Animation
    //svg.selectAll("rect")
    //    .transition()
    //    .duration(800)
    //    .attr("y", function(d) { return y(d.count); })
    //    .attr("height", function(d) { return h - y(d.count); })
    //    .delay(function(d,i){console.log(i) ; return(i*100)})

});
