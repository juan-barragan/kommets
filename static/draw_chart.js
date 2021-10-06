function draw_assets_chart(assets_data, div_name, width, height) {
    nv.addGraph({
        generate: function() {
        		var svg_name = "#"+div_name+" "+"svg";
            var chart = nv.models.multiBarChart()
  						.margin({top: 80, right: 0, bottom: 80, left: 100})
                	.stacked(true);
				chart.xAxis.tickFormat(function(d) { return d3.time.format('%Y')(new Date(d)) });
            var svg = d3.select(svg_name).datum(assets_data);
				svg.append("text")
        			.attr("x", (width / 2))             
        			.attr("y", height)
        			.attr("text-anchor", "right")  
        			.style("font-size", "32px")  
        			.text("Actif");
            svg.transition().duration(0).call(chart).style({ 'width': width, 'height': height });
            nv.utils.windowResize(chart.update);
            return chart;
        }
    });
}
function draw_liabilities_chart(liabilities_data, div_name, width, height) {
    nv.addGraph({
        generate: function() {
        		var svg_name = "#"+div_name+" "+"svg";
            var chart = nv.models.multiBarChart()
  					.margin({top: 80, right: 0, bottom: 80, left: 100})
               .stacked(true);
				chart.xAxis.tickFormat(function(d) { return d3.time.format('%Y')(new Date(d)) });
				var svg = d3.select(svg_name).datum(liabilities_data);
				svg.append("text")
        			.attr("x", (width / 2))             
        			.attr("y", height)
        			.attr("text-anchor", "right")  
        			.style("font-size", "32px")  
        			.text("Passif");          
            svg.transition().duration(0).call(chart).style({ 'width': width, 'height': height });
            nv.utils.windowResize(chart.update);
            return chart;
        }
    });
 }

function draw_revenues_rentability(data, div_name, width, height) {

	var svg_name = "#"+div_name+" "+"svg";
  	//var dates = [new Date(2013,1,1).getTime(),  new Date(2014,1,1).getTime(), new Date(2015,1,1).getTime()];
  	var dates = [data[0].values[0]["x"], data[0].values[1]["x"], data[0].values[2]["x"]];
   data[0].type = "line";
	data[0].yAxis = 1;
   data[1].type = "line";
   data[1].yAxis = 2;
   nv.addGraph(function() {
        	var chart = nv.models.multiChart()
            .margin({top: 80, right: 100, bottom: 80, left: 100})
            .color(d3.scale.category10().range());
            
         
        	chart.xAxis.tickFormat(function(d) { return d3.time.format('%Y')(new Date(d)) });
  			
  			chart.xAxis.tickPadding(25);
        	chart.yAxis1.tickFormat(d3.format(',.1f'));
        	chart.yAxis2.tickFormat(function(d) { return d + "%"; });
       	d3.select(svg_name).datum(data).transition().duration(0).call(chart).style({ 'width': width, 'height': height });
			d3.select(svg_name).append("text")
        			.attr("x", (width / 2))             
        			.attr("y", height)
        			.attr("text-anchor", "middle")  
        			.style("font-size", "32px")  
        			.text("Bénéfices/Rentabilité Brute");
         chart.xAxis.tickValues(dates); 
			nv.utils.windowResize(chart.update);
        return chart;
    });
 }

function draw_quantile_position(data, values, div_name, width, height, score, quantilScore) { //, score, quantileScore, width, height) {
	var svg_name = "#"+div_name+" "+"svg";
   nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .margin({top: 30, right: 80, bottom: 200, left: 100})
            .showValues(true)
				.showXAxis(false)
            .duration(0);
            
        chart.tooltip.contentGenerator(function (obj) {
	        return obj.data.label +": "+ values[obj.index]; 
        });
			d3.select(svg_name).append("text")
        			.attr("x", (width / 2))             
        			.attr("y", 25)
        			.attr("text-anchor", "middle")  
        			.style("font-size", "32px")  
        			.text("Positionnement");            
            
        var svg = d3.select(svg_name)
            .datum(data)
            .call(chart).style({ 'width': 800, 'height': 500 });
        var gradient = svg
    			.append("linearGradient")
    			.attr("x1", "0%")
    			.attr("y1", "0%")
    			.attr("x2", "100%")
    			.attr("y2", "100%")
    			.attr("id", "gradient")
    			.attr("gradientUnits", "userSpaceOnUse");
    		
    		gradient.append("stop").attr("offset", "20%").attr("stop-color", "#f00");
    		gradient.append("stop").attr("offset", "70%").attr("stop-color", "#0f0");

  			var rectangle = svg.append("rect")
                            .attr("x", 0)
                            .attr("y", 455)
                            .attr("width", 600)
                            .attr("height", 20)
                            .attr("fill", "url(#gradient)");
        	svg.append("line")
      		.attr("x1", quantilScore*600)
      		.attr("y1", 450)
      		.attr("x2", quantilScore*600) 
      		.attr("y2", 480)
      		.style("stroke-width", 6)
      		.style("stroke", "blue")
      		.style("fill", "none");
      	svg.append("text")
      		.attr("class", "subtitle")
      		.attr("x", 0)
      		.attr("y", 440)
      		.text("Score: ".concat(score));
      		    
			nv.utils.windowResize(chart.update);
         return chart;
	});
}