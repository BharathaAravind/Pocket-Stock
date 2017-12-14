  $( function() {
    var availableTags=[];
   $.ajax({url: "/getCompanies", success: function(result){
            console.log(result);

            $.each(result, function(key,value) {
                availableTags.push(value);
            });
        }});

    $( "#tags" ).autocomplete({
      source: availableTags
    });
  } );
