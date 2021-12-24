// TO RUN SERVER:
    // terminal python3 -m http.server


//set margin and sizes
var margin = {top:10, bottom:75, right:30, left:30};
var w = 600 - margin.left - margin.right;
var h = 400 - margin.top - margin.bottom;

//append svg
var svg = d3.select('#activity_bar')
    .append('svg')
    .attr('width', w + margin.left + margin.right)
    .attr('height', h + margin.top + margin.bottom)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

//append tooltip
var tooltip = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

//parse data with chart building within
//d3.json('StravaDash/aggData/active_cnt.json', function(data) {
d3.csv('active_cnt2.csv', function(data) {

    console.log(data)
    console.log(2)

    //Add axes
    var x = d3.scaleBand()
        .range([0, w])
        .domain(data.map(function(d) { return d.activity_type; }))
        .padding(0.2);
    
    svg.append('g')
        .attr('id', 'x-ax')
        .attr("transform", "translate(0," + h + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");
    
    var y = d3.scaleLinear()
        .domain([0, 365])//d3.max(data, function(d) { return d.activity_count; })])
        .range([ h, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // Add Bars
    svg.selectAll('active_bars')
        .data(data)
        .enter()
        .append("rect")
            .attr('class', 'barRect')
            .attr("x", function(d) { return x(d.activity_type); })
            .attr("width", x.bandwidth())
            .attr("fill", "#468fa2")
            // no bar at the beginning due to using animation, thus:
            .attr("height", function(d) { return 0; }) // always equal to 0
            .attr("y", function(d) { return h; })
            //tooltip events
            .on("mouseover", function(d) {		
                tooltip.transition()		
                    .duration(200)		
                    .style("opacity", .9);	
                tooltip.html(d.activity_type + ': ' + d.activity_count)	
                    .attr("left", (d3.eventX) + "px")		
                    .attr("top", (d3.eventY - 28) + "px");
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(200)
                    .style('opacity', 0)
            });

    // Animation
    svg.selectAll("rect")
        .transition()
        .duration(1000)
        .attr("y", function(d) { return y(d.activity_count); })
        .attr("height", function(d) { return h - y(d.activity_count); })
        .delay(function(d,i){console.log(i) ; return(i*100)})

});
