function GetSearchParams(searchOptionsDiv){
    var parameters = {};
    // Go through search options and create parameters based on selections
    $(searchOptionsDiv).children().each((idx,element) => {
        var id = $(element).attr("id");
        var value = $(element).val();
        parameters[id] = value;
    });
    console.log(parameters)
    //GetResults(parameters)
}

