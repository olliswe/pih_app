$("#id_departure_place").click(function(){
    var value = $(this).children("option:selected").val();
    if (value == "other"){
        $("#other_place_group").css("display","block");
    }
    else {
        $("#other_place_group").css("display","none");
    }
});

