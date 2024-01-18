var pivot1 = new WebDataRocks({
    container: "#fusionchartArea",
    toolbar: false,
    "height": 400,
    report: {
        "dataSource": {
            "dataSourceType": "json",
            "data": getJSONhelpData()
        },
        "slice": {
             "rows": [{
                 
                 
                "uniqueName": "name"
                 
             },
             {
            "uniqueName": "help"
            }],
            "columns": [{
                "uniqueName": "task"
            }],
            "measures": [{
                "uniqueName": "help",
                "aggregation": "sum"
            }]
        }
    },
    reportcomplete: function() {
        pivot1.off("reportcomplete");
        createBarChart();
  
    }
});



var pivot = new WebDataRocks({
    container: "#wdr-component",
    toolbar: false,
    "height": 400,
    report: {
        "dataSource": {
            "dataSourceType": "json",
            "data": getJSONData()
        },
        "slice": {
             "rows": [{
                 
                 
                "uniqueName": "name"
                 
             },
             {
            "uniqueName": "Measures"
            }],
            "columns": [{
                "uniqueName": "task"
            }],
            "measures": [{
                "uniqueName": "Done",
                "aggregation": "sum"
            }]
        }
    },
    reportcomplete: function() {
        pivot.off("reportcomplete");
        // createAreaChart();
        
        createPieChart();
    }
});




// function createAreaChart() {
//     var chart = new FusionCharts({
//         type: "area2d",
//         renderAt: "fusionchartArea",
//         width: "100%",
//         height: 400
//     });
//     pivot.fusioncharts.getData({
//     type: chart.chartType(), "slice": {
//         "rows": [
//             {
//                 "uniqueName": "name"
//             }
//         ],
//         "columns": [
//             {
//                 "uniqueName": "task"
//             }
//         ],
//         "measures": [
//             {
//                 "uniqueName": "Done",
//                 "aggregation": "sum"
//             }
//         ]
//     }
// 	}, function(data) {
//         chart.setJSONData(data);
//         chart.setChartAttribute("theme", "fusion");
//         chart.setChartAttribute("caption", "Total Revenue by Month");
//         chart.render();
//     });
// }

function createBarChart() {
    var chart = new FusionCharts({
        type: 'mscolumn2d',
        renderAt: "fusionchartBar",
        width: "100%",
        height: 400
    });
    pivot1.fusioncharts.getData({
        type: chart.chartType()
        }, function(data) {
        chart.setJSONData(data);
        chart.setChartAttribute("theme", "fusion");
        chart.setChartAttribute("caption", "Total Revenue by City");
        chart.setChartAttribute("paletteColors", "#9d87f5, #faa27f, #9afa7f, #e37ffa, #7de1fa, #f8fa7f");
        chart.render();
    });
    
}

function createPieChart() {
    var chart = new FusionCharts({
        type: "pie2d",
        renderAt: "fusionchartPie",
        width: "100%",
        height: 400
    });
    
    pivot.fusioncharts.getData({
        type: chart.chartType(), "slice": {
            "rows": [
                {
                    
                    "uniqueName": "task"
                }
            ],
            "columns": [
                {
                    "uniqueName": "ID"
                }
            ],
            "measures": [
                {
                    "uniqueName": "Done",
                    "aggregation": "sum"
                }
            ]
        }
        },
        function(data) {
            chart.setJSONData(data);
            chart.setChartAttribute("theme", "fusion");
            chart.setChartAttribute("caption", "Total Revenue for Each Model");
            chart.setChartAttribute("paletteColors", "#bc5cdb, #493999, #8790a8");
            chart.render();
        }
    
        );
    }

function getJSONData() {
    return [
             {
               "task": "Data structure",
               "ID": "14",
               "name": "Abiel",
               "Done": 1,
               
             },
             {
               "task": "Data structure",
               "ID": "11",
               "name": "Abiel",
               "Done": 0
             },
             {
                "task": "Data structure",
                "ID": "12",
                "name": "Awet",
                "Done": 1
              },
              {
                "task": "Data structure",
                "ID": "13",
                "name": "Murad",
                "Done": 1
              },
            
              {
                "task": "Software",
                "ID": "11",
                "name": "Abiel",
                "Done": 1
              },
              {
                 "task": "Software",
                 "ID": "12",
                 "name": "Awet",
                 "Done": 1
               },
               {
                 "task": "Software",
                 "ID": "13",
                 "name": "Murad",
                 "Done": 0
               }
           ]
}

function getJSONhelpData() {
    return [
             {
               "task": "Data structure",
               "ID": "11",
               "name": "Abiel",
               "help": "Syntax"
               
             },
             {
                "task": "Data structure",
                "ID": "13",
                "name": "Murad",
                "help": "Logical"
              },
             {
               "task": "Data structure",
               "ID": "11",
               "name": "Abiel",
               "help": "Logical"
             },
             {
                "task": "Data structure",
                "ID": "11",
                "name": "Abiel",
                "help": "Syntax"
              },
             {
                "task": "Data structure",
                "ID": "12",
                "name": "Awet",
                "help": "Syntax"
              },
              {
                "task": "Data structure",
                "ID": "13",
                "name": "Murad",
                "help": "Logical"
              },
              {
                "task": "Data structure",
                "ID": "13",
                "name": "Murad",
                "help": "Logical"
              },
              {
                "task": "Software",
                "ID": "11",
                "name": "Abiel",
                "help": "Logical"
              },
              {
                 "task": "Software",
                 "ID": "12",
                 "name": "Awet",
                 "help": "Logical"
               },
               {
                "task": "Software",
                "ID": "12",
                "name": "Awet",
                "help": "Syntax"
               },
               {
                 "task": "Software",
                 "ID": "13",
                 "name": "Murad",
                 "help": "Logical"
               }
           ]
}