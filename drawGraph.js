function drawGraph() {
        var stack = d3.stack();

        var area = d3.area()
            .x(function(d, i) { return x(i); })
            .y0(function(d) { return y(d[0]); })
            .y1(function(d) { return y(d[1]); })
            .curve(d3.curveStepAfter);

        var g = svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          g.append("g")
          .attr("class", "axis axis--x")
          .attr("transform", "rotate(-90)")
          .call(d3.axisBottom(x).ticks(0));


        var entradoEnGrafico = false;
        data = formatForMainGraph(rawData, normalizarPorcentaje);


        var languages = []
        for (var i = 0, n = data.length-1; i < n; ++i) languages.push(data[i].language);
        keys = ["Other", "Germanic", "Romance"]

        x.domain(d3.extent(data, function(d,i) { return i; }));
        y.domain([0,d3.max(d3.extent(data, function(d,i) { return (d["Germanic"]+d["Romance"]+d["Other"]); }))]);
        z.domain(keys);
        stack.keys(keys);

        svg.append("text")
            .text("Effects of Maternal Tongue on English Vocabulary")
            .style("font", "20px sans-serif")
            .style("text-anchor", "middle")
            .attr("x", margin.left + width/2)
            .attr("y", margin.top*2);

        layer = g.selectAll(".layer")
            .data(stack(data))
            .enter().append("g")
            .attr("class", "layer");

        layer.append("path")
        .attr("class", "area")
        .style("fill", function(d) { return z(d.key); })
        .attr("d", area);


        h = svg.append("g").attr("class", "graph")
            .on("mouseleave", function() {entradoEnGrafico = false;})
            .on("mouseenter", function() {entradoEnGrafico = true;})
            .on("click", function() {
                if (shaderInteractivo) {
                    if (distributionDrawn) {
                        distributionDrawn = false;
                        d3.selectAll(".shader").style("pointer-events", "auto");
                        d3.selectAll(".distribution").remove();
                        d3.selectAll("text.xLabel").transition().style("font-weight", "normal");
                    } else distributionDrawn = true;
                }
            });

        h.selectAll(".shader")
            .data(languages).enter().append("rect")
            .attr("x", function(d,i) {return margin.left + i*width/(languages.length/2);})
            .attr("y", margin.top)
            .attr("height", height)
            .attr("class", "shader")
            .attr("width", width / (languages.length/2))
            .style("fill", "white")
            .attr("fill-opacity", "0")
            .on("mouseenter", function(d,i) {
              if (shaderInteractivo) {
                    d3.selectAll(".shader").transition().attr("fill-opacity", "0.4");
                    d3.select(this).transition().attr("fill-opacity", "0");
              }
            })
            .on("mouseleave", function(d) {
              if (shaderInteractivo) {
                  if (entradoEnGrafico) d3.selectAll(".shader").transition().attr("fill-opacity", "0");
                  else d3.select(this).transition().attr("fill-opacity", "0.4");
            }})
            .on("click", function(d,i) {
              if (shaderInteractivo) {
              if (!distributionDrawn) {
                  d3.selectAll(".shader").style("pointer-events", "none").transition().attr("fill-opacity", "0");
                  drawDistribution(rawData,languages[i]);
                  d3.selectAll("text.xLabel").filter(function (d, i2) { return i2 === i;}).transition().style("font-weight", "bold");
                }
            }});

        svg.selectAll("text.xLabel")
            .data(languages).enter()
            .append("text")
            .attr("class", "xLabel")
            .style("font", "14px sans-serif")
            .attr("y", height + margin.top + (margin.bottom/2))
            .attr("x", function(d, i) { return margin.left*2 + i*width/(languages.length/2);})
            .style("text-anchor", "end")
            .attr("transform", function(d,i) {return "translate(" + (0+width/(2*(data.length-1)))  + ",0) " + "rotate(-40 " + String(margin.left + i*width/((data.length-1)/2)) + " " + String(height + margin.top + (margin.bottom/2)) + ")";})
            .text(function(d, i) { return languages[i].charAt(0).toUpperCase() + languages[i].slice(1);});
        transladarGrafico(0);
}


function formatForMainGraph(rawData, showPercentage) {
  var languages = []
  for (language in rawData) languages.push(language);
  data = []
    for (var i = 0, n = languages.length; i < n; ++i) {
        data[i] = {};
        data[i]['language'] = languages[i];
        data[i]['Germanic'] = rawData[languages[i]]['germanic_Count'];
        data[i]['Romance'] = rawData[languages[i]]['romance_Count'];
        data[i]['Other'] = rawData[languages[i]]['other_Count'];
        if (showPercentage) {
            var total = data[i]['Germanic'] + data[i]['Romance'] + data[i]['Other'];
            data[i]['Germanic'] = data[i]['Germanic'] / total * 100;
            data[i]['Romance'] = data[i]['Romance'] / total * 100;
            data[i]['Other'] = data[i]['Other'] / total * 100;
        }
    }
    //creating a duplicate results in the correct output from stack
    data[languages.length] = {};
    data[languages.length]['language'] = languages[languages.length-1];
    data[languages.length]['Germanic'] = rawData[languages[languages.length-1]]['germanic_Count'] / 1000;
    data[languages.length]['Romance'] = rawData[languages[languages.length-1]]['romance_Count'] / 1000;
    data[languages.length]['Other'] = rawData[languages[languages.length-1]]['other_Count'] / 1000;

    return data;
}


function drawDistribution(rawData, language) {
    d3.select("g.graph").append("rect").attr("class", "distribution")
        .attr("width", width - 60)
        .attr("height", height - 60)
        .attr("x", margin.left + 30)
        .attr("y", margin.top + 30)
        .attr("fill", "white")
        .attr("fill-opacity", "0")
        .transition()
            .attr("fill-opacity", "1")
            .attr("style", "stroke:black");
    var max = 0;
    var langCount = 0;
    var germanicArray = [];
    var romanceArray = [];
    var otherArray = [];
    for (lang in rawData[language]["germanic"]) {
        if (rawData[language]["germanic"][lang] > max) max = rawData[language]["germanic"][lang];
        ++langCount;
        germanicArray.push({"language":lang, "count":rawData[language]["germanic"][lang]})
    }
    for (lang in rawData[language]["romance"]) {
        if (rawData[language]["romance"][lang] > max) max = rawData[language]["romance"][lang];
        ++langCount;
        romanceArray.push({"language":lang, "count":rawData[language]["romance"][lang]})
    }
    for (lang in rawData[language]["other"]) {
        if (rawData[language]["other"][lang] > max) max = rawData[language]["other"][lang];
        ++langCount;
        otherArray.push({"language":lang, "count":rawData[language]["other"][lang]})

    }

    yScale = d3.scaleLinear().domain([0, max]).range([0, height - 215]);


    var barsPresent = 0;
    var textPresent = 0;
    svg.selectAll("rect.distributionBar")
        .data(germanicArray).enter().append("rect")
        .attr("x", function(d, i ) { return 5+margin.left + 30 + barsPresent++ *((width - 60) / langCount) ;})
        .attr("y", function(d) { return margin.top + 30 + (height - 60) - yScale(d.count);})
        .attr("height", function(d) { return yScale(d.count);})
        .attr("width", ((width - 60) / langCount) - 10)
        .transition()
        .style("pointer-events", "none")
        .attr("class", "distribution")
        .attr("fill","orange");

    svg.selectAll("text.distributionText")
        .data(germanicArray).enter().append("text")
        .attr("y", function(d, i ) { return 5+margin.left+30 + textPresent++ *((width - 60) / langCount) +((width - 60) / langCount)/2 ;})
        .attr("x", function(d) { return -(margin.top + 30 + (height - 60) - yScale(d.count))+5;})
        .attr("transform", "rotate(-90)")
        .transition()
        .attr("class", "distribution")
        .text(function(d) {
            var cnt = d.count;
            var retval = d.language + ": ";
            if (cnt == 0) return (retval + ">0.01%");
            retval += String(Math.round(10000*d.count/rawData[language]["total_Count"])/100) + " %";
            return retval});

    svg.selectAll("rect.distributionBar")
        .data(romanceArray).enter().append("rect")
        .attr("x", function(d, i ) { return 5+margin.left + 30 + barsPresent++ *((width - 60) / langCount) ;})
        .attr("y", function(d) { return margin.top + 30 + (height - 60) - yScale(d.count);})
        .attr("height", function(d) { return yScale(d.count);})
        .attr("width", ((width - 60) / langCount) - 10)
        .transition()
        .style("pointer-events", "none")
        .attr("class", "distribution")
        .attr("fill","green");

    svg.selectAll("text.distributionText")
        .data(romanceArray).enter().append("text")
        .attr("y", function(d, i ) { return 5+margin.left + 30 + textPresent++ *((width - 60) / langCount) +((width - 60) / langCount)/2 ;})
        .attr("x", function(d) { return -(margin.top + 30 + (height - 60) - yScale(d.count))+5;})
        .attr("transform", "rotate(-90)")
        .transition()
        .attr("class", "distribution")
        .text(function(d) {
            var cnt = d.count;
            var retval = d.language + ": ";
            if (cnt == 0) return (retval + ">0.01%");
            retval += String(Math.round(10000*d.count/rawData[language]["total_Count"])/100) + " %";
            return retval});

    svg.selectAll("rect.distributionBar")
        .data(otherArray).enter().append("rect")
        .attr("x", function(d, i ) { return 5+margin.left + 30 + barsPresent++ *((width - 60) / langCount) ;})
        .attr("y", function(d) { return margin.top + 30 + (height - 60) - yScale(d.count);})
        .attr("height", function(d) { return yScale(d.count);})
        .attr("width", ((width - 60) / langCount) - 10)
        .transition()
        .style("pointer-events", "none")
        .attr("class", "distribution")
        .attr("fill","blue");

    svg.selectAll("text.distributionText")
        .data(otherArray).enter().append("text")
        .attr("y", function(d, i ) { return 5+margin.left + 30 + textPresent++ *((width - 60) / langCount) +((width - 60) / langCount)/2 ;})
        .attr("x", function(d) { return -(margin.top + 30 + (height - 60) - yScale(d.count))+5;})
        .attr("transform", "rotate(-90)")
        .transition()
        .attr("class", "distribution")
        .text(function(d) {
            var cnt = d.count;
            var retval = d.language + ": ";
            if (cnt == 0) return (retval + ">0.01%");
            retval += String(Math.round(10000*d.count/rawData[language]["total_Count"])/100) + " %";
            return retval});}

function transladarGrafico(distancia) {
    shaderInteractivo = false; //congela interactivida, no se puede user
    //pointer-events porque no se aplica al svg de nivel raiz: esto impide
    // intentos de phishing con SVGs en capas
    d3.selectAll(".layer").transition().attr("transform", "translate(" + distancia + ",0)");
    d3.selectAll(".shader").transition().attr("transform", "translate(" + distancia + ",0)")
    .attr("x", function(d,i) {return margin.left + i*width/((data.length-1)/2);})
    d3.selectAll(".xLabel").attr("transform", "")
        .attr("y", height + margin.top + (margin.bottom/2))
        .attr("x", function(d, i) { return margin.left*2 + i*width/((data.length-1)/2);})
        .transition()
        .style("opacity", function(d, i) {if ((distancia < 0 && (i >= (data.length-1)/2))) return 1;
                                       if ((distancia == 0 && (i < (data.length-1)/2))) return 1;
                                       else return 0})
        .attr("transform", function(d,i) {return "translate(" + (distancia+width/(2*(data.length-1)))
        + ",0) " + "rotate(-40 " + String(margin.left + i*width/((data.length-1)/2)) + " "
        + String(height + margin.top + (margin.bottom/2)) + ")";});
    shaderInteractivo = true;
    if (distancia == 0) dibujarEjeY(0);
    else dibujarEjeY(1);
}


function scalarGrafico() {
    transladarGrafico(0);
    shaderInteractivo = false;
    d3.selectAll(".layer").transition().attr("transform", "scale(" + 0.5 +",1)");
    d3.selectAll(".shader").transition().attr("transform", "scale(" + 0.5 +",1)")
    .attr("x", function(d,i) {return margin.left*2 + 2*i*(width/(data.length-1));});
    d3.selectAll(".xLabel").transition()
        .style("opacity", 1)
        .attr("y", height + margin.top + (margin.bottom/2))
        .attr("x", function(d, i) { return margin.left*2 + i*width/((data.length-1));})
            .attr("transform", function(d,i) {
                return "translate(" + (0+width/(4*(data.length-1)) - 50)  + ",-60) "
                  + "rotate(-40 " + String(margin.left*2 + i*width/((data.length-1)))
                  + " " + String(height + margin.top + (margin.bottom/2)) + ")";})

    shaderInteractivo = true;
    dibujarEjeY(0);

}

function dibujarEjeY(ubicacionRotulo) {
    //curbir la parte del Grafico que se ve detras del eje:
    d3.selectAll(".rectCubertador").remove();
    d3.selectAll(".axis--y").remove();
    d3.selectAll(".rotuloY").remove();
    d3.selectAll(".rotuloCapa").remove();
    svg.append("rect")
        .attr("class", "rectCubertador")
        .attr("x",0)
        .attr("x",0)
        .attr("width", margin.left)
        .attr("height", height + margin.bottom/2)
        .style("fill", "white");
    svg.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y))
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    svg.append("text")
        .attr("class", "rotuloY")
        .attr("transform", "rotate(-90)") //gira alrededor del origen
        .text(function() {if (normalizarPorcentaje) return "Percentage of Etymologies (%)"
                          else return "Sample Size of Unique Relevant Words";})
        .style("font", "14px sans-serif")
        .attr("text-anchor", "middle")
        .attr("x", -height/2)
        .attr("y", 3*margin.left/5);
    svg
        .append("text")
        .attr("class", "rotuloCapa")
        .attr("x", 1.5*margin.left)
        .attr("y", 266)
        .text(function(d) { "Romance" });
}

function toggleGraphPercentage() {
    normalizarPorcentaje = !normalizarPorcentaje;
    data = formatForMainGraph(rawData, normalizarPorcentaje);
    d3.selectAll(".layer").remove();
    d3.selectAll(".axis--x").remove();
    d3.selectAll(".graph").remove();
    drawGraph(rawData);
}
