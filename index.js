function SearchEvents(searchOptionsDiv){
    var parameters = GetSearchParams(searchOptionsDiv);
    
    //run API calls
    var resultsData = [{id:"1"},{id:"2"},{id:"3"}];
    PopulateResults(resultsData)
}

function GetSearchParams(searchOptionsDiv){
    // Go through search options and create parameters based on selections
    var parameters = {};
    $(searchOptionsDiv).children().each((idx,element) => {
        var id = $(element).attr("id");
        var value = $(element).children(".form-select").val();
        parameters[id] = value;
    });
    console.log(parameters)

    return parameters;
}

function PopulateResults(resultsData){
    // given the JSON data, create results list
    $("#results").empty()
    resultsData.forEach((idx,element) => {
        var resultsDiv = CreateResultsDiv(idx,element);
        $("#results").append(resultsDiv)
    });


}

function CreateResultsDiv(idx,resultInfo){
    var div = `
        <div class="card mb-3" style="max-width: 540px;" id="${idx}">
        <div class="row g-0">
            <div class="col-md-4">
            <img src="..." class="img-fluid rounded-start" alt="...">
            </div>
            <div class="col-md-8">
            <div class="card-body">
                <h5 class="card-title">Event Name</h5>
                <p class="card-text">Event details</p>
                <p class="card-text"><small class="text-body-secondary">1 mi away</small></p>
            </div>
            </div>
        </div>
        </div>
    
    `;

    return div
}
