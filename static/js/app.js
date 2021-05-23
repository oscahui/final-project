console.log("App Ready");

d3.select("#tellMe").on("click", (event) => tellMe(event));
d3.select("#predictType").on("change", disableFields);

d3.select("#alertOutcome").style("display", "none");

// init busy indicator
busyi = new busy_indicator(document.getElementById("busybox"),
    document.querySelector("#busybox div"));

// show / hide other fields
function disableFields() {
    let predictType = d3.select("#predictType").node().value;

    if (predictType === "byvalues") {
        document.getElementById("goldval").disabled = false;
        document.getElementById("compval").disabled = false;
        document.getElementById("induval").disabled = false;
        document.getElementById("oilval").disabled = false;
        document.getElementById("spxval").disabled = false;

    } else {

        document.getElementById("goldval").disabled = true;
        document.getElementById("compval").disabled = true;
        document.getElementById("induval").disabled = true;
        document.getElementById("oilval").disabled = true;
        document.getElementById("spxval").disabled = true;
    }

}

// function for button press
function tellMe(event) {
    init();
    busyi.show();
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
    var timestamp = Date.parse(dateval) * 1000000;
    var data = {};
    var mlRouteString = "";

    console.log(dateval);
    console.log(predictType);

    if (predictType === "byvalues") {
        console.log(predictType);
        data = {
            "gold": parseFloat(goldval),
            "comp": parseFloat(compval),
            "spx": parseFloat(spxval),
            "indu": parseFloat(induval),
            "oil": parseFloat(oilval),
            "timestamp": timestamp,
        }
        mlRouteString = "/predict/feature";
    } else {
        console.log(predictType);
        data = {
            "type": "price",
            "date": dateval,
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

// show returned results
function showResult(data) {
    var bitcoinValue = 0.1;
    var messageprefix = "Bitcoin Value is going";
    let predictType = d3.select("#predictType").node().value;
    let alertOutcomeDisplay = d3.select("#alertOutcome");


    console.log(predictType);
    console.log(data["predict"]);


    var predict = data["predict"];

    if (predictType !== "byvalues") {
        bitcoinValue = parseFloat(predict).toFixed(2);
        messageprefix = "Bitcoin Value will be";
        drawLine(data);
        alertOutcomeDisplay.text(`${messageprefix} ${bitcoinValue}!!!`);
        alertOutcomeDisplay.style("display", "block");
    } else {
        alertOutcomeDisplay.text(`${messageprefix} ${predict}!!!`);
        alertOutcomeDisplay.style("display", "block");
    }

    // var outcome = "Unknown";
    busyi.hide();



}

//build plot for ML results
function drawLine(data) {
    if (data["trend"]) {

        var date = data["trend"].map(d => new Date(d["date"]));
        var latest = new Date(Math.max.apply(null, date));
        latest.setDate(latest.getDate() - 30);

        var month_data = data["trend"].filter(d => (new Date(d["date"]) >= latest));
        var real_data = month_data.filter(d => d["real"] == 1);
        var predict_data = month_data.filter(d => d["real"] == 0);

        var date_real = real_data.map(d => (new Date(d["date"])));

        var price_real = real_data.map(d => d["close"]);

        var date_predict = predict_data.map(d => (new Date(d["date"])));

        var price_predict = predict_data.map(d => d["close"]);

        date_real.push(date_predict[0]);
        price_real.push(price_predict[0]);

        var trace1 = {
            x: date_real,
            y: price_real,
            type: "line",
            name: "actual"
        };

        var trace2 = {
            x: date_predict,
            y: price_predict,
            type: "line",
            name: "predict"
        };

        var layout = {
            title: {
                text: 'Bitcoin Predicted Price',
                font: {
                    family: 'Arial',
                    size: 18,
                    color: 'rgb(0,0,0)'
                }
            },
            paper_bgcolor: 'rgba(255,220,232,.85)',
            margin: {
                l: 55,
                r: 55,
                b: 55,
                t: 55,
                pad: 4
            }
        }

        var config = { responsive: true };

        Plotly.newPlot('line-plot', [trace1, trace2], layout, config);

    }
}

// Build charts
function buildAllBTCChart(dropdown_values) {
    var url = "api/bitcoin/all";

    d3.json(url).then(function (response) {

        var grouped_data = d3.group(response, d => d.btc)

        var traces = Array();

        grouped_data.forEach(element => {
            traces.push({
                x: element.map(d => d.date),
                y: element.map(d => d.close),
                name: element[0].date,
                type: 'line'
            });
        });

        var layout = {
            title: {
                text: 'Bitcoin Price vs Time',
                font: {
                    family: 'Arial',
                    size: 18,
                    color: 'rgb(0,0,0)'
                }
            },
            paper_bgcolor: 'rgba(1,158,124,.85)',
            margin: {
                l: 55,
                r: 55,
                b: 55,
                t: 55,
                pad: 4
            },
            yaxis: {
                title: 'Bitcoin Price in USD'
            },
            xaxis: {
                title: 'Year'
            }
        };

        var config = { responsive: true };

        Plotly.newPlot('bcprice-plot', traces, layout, config);
    });

};

function buildAllGOLDChart(dropdown_values) {
    var url = "api/other/all";

    d3.json(url).then(function (response) {

        var grouped_data = d3.group(response, d => d.other)

        var traces = Array();

        grouped_data.forEach(element => {
            traces.push({
                x: element.map(d => d.date),
                y: element.map(d => d.gold),
                name: element[0].date,
                type: 'bar'
            });
        });

        var layout = {
            barmode: 'stack',
            title: {
                text: 'Gold Price vs Time',
                font: {
                    family: 'Arial',
                    size: 18,
                    color: 'rgb(0,0,0)'
                }
            },
            paper_bgcolor: 'rgba(187,160,8,.60)',
            margin: {
                l: 55,
                r: 55,
                b: 55,
                t: 55,
                pad: 4
            },
            yaxis: {
                title: 'Gold Price'
            },
            xaxis: {
                title: 'Year'
            }
        };

        var config = { responsive: true };

        Plotly.newPlot('goldprice-plot', traces, layout, config);
    });
};


function buildAllOilChart(dropdown_values) {
    var url = "api/other/all";

    d3.json(url).then(function (response) {

        var grouped_data = d3.group(response, d => d.other)

        var traces = Array();

        grouped_data.forEach(element => {
            traces.push({
                x: element.map(d => d.date),
                y: element.map(d => d.gold),
                name: element[0].date,
                type: 'line'
            });
        });

        var layout = {
            title: {
                text: 'Oil Price vs Time',
                font: {
                    family: 'Arial',
                    size: 18,
                    color: 'rgb(0,0,0)'
                }
            },
            paper_bgcolor: 'rgba(150,150,150,.85)',
            margin: {
                l: 55,
                r: 55,
                b: 55,
                t: 55,
                pad: 4
            },
            yaxis: {
                title: 'Oil Price'
            },
            xaxis: {
                title: 'Year'
            }
        };

        var config = { responsive: true };

        Plotly.newPlot('oilprice-plot', traces, layout, config);
    });
}

function init() {
    buildAllBTCChart();
    buildAllGOLDChart();
    buildAllOilChart();
}

