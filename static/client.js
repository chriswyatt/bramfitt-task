const pb = require('./prediction_pb');
const nunjucks = require('nunjucks')

let nunjucksEnv = nunjucks.configure('views',{ autoescape: true });

nunjucksEnv.addFilter('pbDateTime', function(obj) {
    let value = (obj['seconds'] * 1000) + (obj['nanos'] / 1000000);
    return new Date(value);
});

const predictionsUrl = 'http://127.0.0.1:5000/arrivals/490009333W/';
const predictionsListUrl = 'http://127.0.0.1:5000/arrivals/';

function replaceInnerHTML(oldDiv, html) {
    let newDiv = oldDiv.cloneNode(false);
    newDiv.innerHTML = html;
    oldDiv.parentNode.replaceChild(newDiv, oldDiv);
}

function displayGetArrivalPredictionsResponse(responsePb) {
    let logPb = responsePb.getLog();
    let logPbObj = logPb.toObject();
    let predictionsDiv = document.getElementById('div-predictions');

    replaceInnerHTML(
        predictionsDiv,
        nunjucksEnv.render(
            'predictions_request_list.html',
            {'logsList': [logPbObj]},
        ),
    );
}

function displayGetArrivalPredictionsListResponse(responsePb) {
    let responsePbObj = responsePb.toObject();
    let predictionsDiv = document.getElementById('div-predictions');

    replaceInnerHTML(
        predictionsDiv,
        nunjucksEnv.render(
            'predictions_request_list.html',
            responsePbObj,
        ),
    );
}

function onBtnGetPredictionsClick(event) {
    fetch(predictionsUrl)
        .then(response => response.arrayBuffer())
        .then(buffer => pb.GetArrivalPredictionsResponse.deserializeBinary(buffer))
        .then(responsePb => displayGetArrivalPredictionsResponse(responsePb));
}

function onBtnGetPredictionsListClick(event) {
    fetch(predictionsListUrl)
        .then(response => response.arrayBuffer())
        .then(buffer => pb.GetArrivalPredictionsListResponse.deserializeBinary(buffer))
        .then(responsePb => displayGetArrivalPredictionsListResponse(responsePb));
}

function onLoad(event) {
    let btnGetPredictions = document.getElementById("btn-get-predictions");
    btnGetPredictions.addEventListener("click", onBtnGetPredictionsClick);

    let btnGetPredictionsList = document.getElementById("btn-get-predictions-list");
    btnGetPredictionsList.addEventListener("click", onBtnGetPredictionsListClick);
}

window.addEventListener("load", onLoad);
