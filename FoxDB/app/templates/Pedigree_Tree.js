var matGM = {{ maternal_grandmother }}
//var matGM = null;
var matGF = {{ maternal_grandfather }}
//var matGF = null;
var patGM = {{ paternal_grandmother }} 
var patGF = {{ paternal_grandfather }}
var mother = {{ mother }}
var father = {{ father }}
var children = [{% for child in children %}{{ child }}{% endfor %}];

var genThreeCount = children.length;

var svgWidth = 600;
var svgHeight = 600;

var gen1Width = svgWidth/4;
var gen2Width = svgWidth/2;
var gen3Width = svgWidth/genThreeCount;
var genHeight = svgHeight/3;

var gen1Param = Math.min(gen1Width/4,50);
var gen2Param = Math.min(gen2Width/4,50);
var gen3Param = Math.min(gen3Width/4,50);

var connectPt1_x = gen1Width;
var connectPt1_y = genHeight;
var connectPt2_x = 3*gen1Width;
var connectPt2_y = genHeight;
var connectPt3_x = svgWidth/2;
var connectPt3_y = 2*genHeight;


var svgContainer = d3.select("body").append("svg").attr("width",svgWidth).attr("height",svgHeight);

var gen3 = 0;
if(matGM != null){
	var nodeShape = svgContainer.append("circle");
	var shapeAttr = nodeShape.attr("cx", gen1Width/2)
					.attr("cy", genHeight/2)
					.attr("r", gen1Param)
					.style("fill", "red")
					.style("stroke","red")
					.style("stroke-width",2)
					.style("fill-opacity",0.1)
					.style("stroke-opacity",0.7)
	var lineData = [{"x": gen1Width/2+gen1Param, "y": genHeight/2}, {"x": gen1Width, "y": genHeight/2}, {"x": connectPt1_x, "y": connectPt1_y}]
	var lineFunction = d3.svg.line()
                        .x(function(d) { return d.x; })
                        .y(function(d) { return d.y; })
                        .interpolate("linear");
	var lineGraph = svgContainer.append("path")
                        .attr("d", lineFunction(lineData))
                        .attr("stroke", "green")
                        .attr("stroke-width", 2)
                        .attr("fill", "none");
    // var text1 = svgContainer.append('text').text('ID: '+matGM[0])
    //             .attr('x', gen1Width/2-gen1Param)
    //             .attr('y', genHeight/2-5)
    //             .attr('fill', 'black')
    //             .style('font-size', 15);
    var text2 = svgContainer.append('text').text(matGM[5]+"/"+matGM[6])
                .attr('x', gen1Width/2-gen1Param)
                .attr('y', genHeight/2+15)
                .attr('fill', 'black')
}
if(matGF != null){
	var nodeShape = svgContainer.append("rect");
	var shapeAttr = nodeShape.attr("x", gen1Width*3/2-gen1Param)
					.attr("y", genHeight/2-gen1Param)
					.attr("width", gen1Param*2)
					.attr("height", gen1Param*2)
					.style("fill", "blue")
					.style("stroke","blue")
					.style("stroke-width",2)
					.style("fill-opacity",0.1)
					.style("stroke-opacity",0.7)
	var lineData = [{"x": gen1Width*3/2-gen1Param, "y": genHeight/2}, {"x": gen1Width, "y": genHeight/2}, {"x": connectPt1_x, "y": connectPt1_y}]
	var lineFunction = d3.svg.line()
                        .x(function(d) { return d.x; })
                        .y(function(d) { return d.y; })
                        .interpolate("linear");
	var lineGraph = svgContainer.append("path")
                        .attr("d", lineFunction(lineData))
                        .attr("stroke", "green")
                        .attr("stroke-width", 2)
                        .attr("fill", "none");
    // var text1 = svgContainer.append('text').text('ID: '+matGM[0])
    //             .attr('x', gen1Width/2-gen1Param)
    //             .attr('y', genHeight/2-5)
    //             .attr('fill', 'black')
    //             .style('font-size', 15);
    var text2 = svgContainer.append('text').text(matGF[5]+"/"+matGF[6])
                .attr('x', gen1Width*3/2-gen1Param)
                .attr('y', genHeight/2+15)
                .attr('fill', 'black')
}
if(patGM != null){
	var nodeShape = svgContainer.append("circle");
	var shapeAttr = nodeShape.attr("cx", gen1Width*5/2)
					.attr("cy", genHeight/2)
					.attr("r", gen1Param)
					.style("fill", "red")
					.style("stroke","red")
					.style("stroke-width",2)
					.style("fill-opacity",0.1)
					.style("stroke-opacity",0.7)
	var lineData = [{"x": gen1Width*5/2+gen1Param, "y": genHeight/2}, {"x": gen1Width*3, "y": genHeight/2}, {"x": connectPt2_x, "y": connectPt2_y}]
	var lineFunction = d3.svg.line()
                        .x(function(d) { return d.x; })
                        .y(function(d) { return d.y; })
                        .interpolate("linear");
	var lineGraph = svgContainer.append("path")
                        .attr("d", lineFunction(lineData))
                        .attr("stroke", "green")
                        .attr("stroke-width", 2)
                        .attr("fill", "none");
    // var text1 = svgContainer.append('text').text('ID: '+matGM[0])
    //             .attr('x', gen1Width/2-gen1Param)
    //             .attr('y', genHeight/2-5)
    //             .attr('fill', 'black')
    //             .style('font-size', 15);
    var text2 = svgContainer.append('text').text(patGM[5]+"/"+patGM[6])
                .attr('x', gen1Width*5/2-gen1Param)
                .attr('y', genHeight/2+15)
                .attr('fill', 'black')
}
if(patGF != null){
	var nodeShape = svgContainer.append("rect");
	var shapeAttr = nodeShape.attr("x", gen1Width*7/2-gen1Param)
					.attr("y", genHeight/2-gen1Param)
					.attr("width", gen1Param*2)
					.attr("height", gen1Param*2)
					.style("fill", "blue")
					.style("stroke","blue")
					.style("stroke-width",2)
					.style("fill-opacity",0.1)
					.style("stroke-opacity",0.7)
	var lineData = [{"x": gen1Width*7/2-gen1Param, "y": genHeight/2}, {"x": gen1Width*3, "y": genHeight/2}, {"x": connectPt2_x, "y": connectPt2_y}]
	var lineFunction = d3.svg.line()
                        .x(function(d) { return d.x; })
                        .y(function(d) { return d.y; })
                        .interpolate("linear");
	var lineGraph = svgContainer.append("path")
                        .attr("d", lineFunction(lineData))
                        .attr("stroke", "green")
                        .attr("stroke-width", 2)
                        .attr("fill", "none");
    // var text1 = svgContainer.append('text').text('ID: '+matGM[0])
    //             .attr('x', gen1Width/2-gen1Param)
    //             .attr('y', genHeight/2-5)
    //             .attr('fill', 'black')
    //             .style('font-size', 15);
    var text2 = svgContainer.append('text').text(patGF[5]+"/"+patGF[6])
                .attr('x', gen1Width*7/2-gen1Param)
                .attr('y', genHeight/2+15)
                .attr('fill', 'black')
}
if(mother != null){
	var nodeShape = svgContainer.append("circle");
	var shapeAttr = nodeShape.attr("cx", gen2Width/2)
					.attr("cy", 3/2*genHeight)
					.attr("r", gen2Param)
					.style("fill", "red")
					.style("stroke","red")
					.style("stroke-width",2)
					.style("fill-opacity",0.1)
					.style("stroke-opacity",0.7)
	var topLineData = [{"x": gen2Width/2, "y": 3/2*genHeight-gen2Param}, {"x": connectPt1_x, "y": connectPt1_y}]
	var bottomLineData = [{"x": gen2Width/2+gen2Param,"y": 3/2*genHeight},{"x": gen2Width,"y": 3/2*genHeight},{"x": connectPt3_x,"y": connectPt3_y}]	
	var lineFunction = d3.svg.line()
                         .x(function(d) { return d.x; })
                         .y(function(d) { return d.y; })
                         .interpolate("linear");
    var topLineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(topLineData))
                            .attr("stroke", "green")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
    var bottomLineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(bottomLineData))
                            .attr("stroke", "green")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
    // var text1 = svgContainer.append('text').text('ID: '+currentSample[0])
    //             .attr('x', gen2Width*gen2+gen2Width/2-gen2Param)
    //             .attr('y', genHeight*3/2-5)
    //             .attr('fill', 'black')
    var text2 = svgContainer.append('text').text(mother[5]+"/"+mother[6])
                .attr('x', gen2Width/2-gen2Param)
                .attr('y', genHeight*3/2+15)
                .attr('fill', 'black')
}
if(father != null){
	var nodeShape = svgContainer.append("rect");
	var shapeAttr = nodeShape.attr("x", gen2Width*3/2-gen2Param)
					.attr("y", 3/2*genHeight-gen2Param)
					.attr("width", gen2Param*2)
					.attr("height", gen2Param*2)
					.style("fill", "blue")
					.style("stroke","blue")
					.style("stroke-width",2)
					.style("fill-opacity",0.1)
					.style("stroke-opacity",0.7)
	var topLineData = [{"x": 3/2*gen2Width, "y": 3/2*genHeight-gen2Param}, {"x": connectPt2_x, "y": connectPt2_y}]
	var bottomLineData = [{"x": 3/2*gen2Width-gen2Param,"y": 3/2*genHeight},{"x": gen2Width,"y": 3/2*genHeight},{"x": connectPt3_x,"y": connectPt3_y}]
	var lineFunction = d3.svg.line()
                         .x(function(d) { return d.x; })
                         .y(function(d) { return d.y; })
                         .interpolate("linear");
    var topLineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(topLineData))
                            .attr("stroke", "green")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
    var bottomLineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(bottomLineData))
                            .attr("stroke", "green")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
    // var text1 = svgContainer.append('text').text('ID: '+currentSample[0])
    //             .attr('x', gen2Width*gen2+gen2Width/2-gen2Param)
    //             .attr('y', genHeight*3/2-5)
    //             .attr('fill', 'black')
    var text2 = svgContainer.append('text').text(father[5]+"/"+father[6])
                .attr('x', gen2Width*3/2-gen2Param)
                .attr('y', genHeight*3/2+15)
                .attr('fill', 'black')
}

for(i=0; i<children.length; i++){
	var currentSample = children[i];

	if(currentSample[2] == 1){ // male, create a square
			var nodeShape = svgContainer.append("rect");
			var shapeAttr = nodeShape.attr("x", gen3Width*gen3+gen3Width/2-gen3Param)
									.attr("y", 5/2*genHeight-gen3Param)
									.attr("width", gen3Param*2)
									.attr("height", gen3Param*2)
									.style("fill", "blue")
									.style("stroke","blue")
									.style("stroke-width",2)
									.style("fill-opacity",0.1)
									.style("stroke-opacity",0.7)
	}else{ // female, create a circle
			var nodeShape = svgContainer.append("circle");
			var shapeAttr = nodeShape.attr("cx", gen3Width*gen3+gen3Width/2)
									.attr("cy", 5/2*genHeight)
									.attr("r", gen3Param)
									.style("fill", "red")
									.style("stroke","red")
									.style("stroke-width",2)
									.style("fill-opacity",0.1)
									.style("stroke-opacity",0.7)
	}
	gen3++;
		
		
		var lineData = [{"x": gen3Width*gen3-gen3Width/2,"y": 5/2*genHeight-gen3Param},{"x": gen3Width*gen3-gen3Width/2,"y": 2*genHeight},{"x": connectPt3_x,"y": connectPt3_y}]
		var lineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(lineData))
                            .attr("stroke", "green")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
        var lineGraph = svgContainer.append("path")
                            .attr("d", lineFunction(lineData))
                            .attr("stroke", "green")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
        var text1 = svgContainer.append('text').text('ID: '+currentSample[0])
                 .attr('x', gen3Width*(gen3-1)+gen3Param)
                 .attr('y', genHeight*5/2-5)
                 .attr('fill', 'black');
        var text2 = svgContainer.append('text').text(currentSample[5]+"/"+currentSample[6])
                .attr('x', gen3Width*(gen3-1)+gen3Param)
                .attr('y', genHeight*5/2+15)
                .attr('fill', 'black')
}
