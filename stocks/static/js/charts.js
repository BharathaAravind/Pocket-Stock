
function displayGraph(data){
var ctx = document.getElementById("myChart").getContext('2d');
var lowData = [];
var labels = [];
var closeData = [];
var highData = [];
//console.log(data);
for(var key in data){
    labels.push(key);
    highData.push(data[key]["highPrice"]);
    lowData.push(data[key]["lowPrice"]);
    closeData.push(data[key]["closePrice"]);
}

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'High',
            data: highData,
            borderColor: 'rgba(255,99,132,0.7)',
            borderWidth: 1,
            fill: false,
        },
        {
            label: 'Low',
            data: lowData,
            borderColor: 'rgba(0,255,0,0.7)',
            borderWidth: 1,
            fill: false
        },{
            label: 'Close',
            data: closeData,
            borderColor: 'rgba(0,0,255,0.7)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    autoSkip:true,
                    stepSize:10,
                    maxTickLimit: 20
                }
            }]
        }
    }
});
}
