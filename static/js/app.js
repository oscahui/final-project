console.log("App Ready");

d3.select("#tellMe").on("click", (event) => tellMe(event));

d3.select("#alertOutcome").style("display", "none");

function tellMe(event) {
    d3.event.preventDefault();
    d3.select("#alertOutcome").style("display", "none");
    console.log("Checking Bitcoin Price");

    let predictType = d3.select("#predictType").node().value;
    let dateval = d3.select("#dateval").node().value;
    let goldval = d3.select("#goldval").node().value;
    let compval = d3.select("#compval").node().value;
    let induval = d3.select("#induval").node().value;
    let oilval = d3.select("#oilval").node().value;
    let spxval = d3.select("#spxval").node().value;
    var timestamp = Date.parse(dateval)*1000000;
    var data = {};
    var mlRouteString = "";
    
    console.log(dateval);
    console.log(predictType);
 {}
    if (predictType === "byvalues"){
        console.log(predictType);
        data = {
            "gold": parseFloat(goldval),
            "comp": parseFloat(compval),
            "spx" : parseFloat(spxval),
            "indu" : parseFloat(induval),
            "oil" : parseFloat(oilval),
            "timestamp" : timestamp,
        }
        mlRouteString = "/predict/feature";
    } else {
        console.log(predictType);
        data = {
            "type" : "price",
            "date" : dateval,
        }
        mlRouteString = "/predict/date";
    }


    console.log(data);

    d3.json(
        mlRouteString, {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }
    ).then(
        (data) => showResult(data)
    );

}

function showResult(data) {
    console.log("showResult");
    console.log(data["predict"]);
    var predict = data["predict"];

    // var outcome = "Unknown";
    let alertOutcomeDisplay = d3.select("#alertOutcome");

    alertOutcomeDisplay.text(`Bitcoin Value is going ${data["predict"]}!!!!!!`);
    alertOutcomeDisplay.style("display", "block");

}