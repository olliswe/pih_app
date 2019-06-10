$("#id_expenses_covered_by").click(function(){
    var value = $(this).children("option:selected").val();
    if (value == "Covered by us but reimbursed" || value == "Covered by us (not reimbursed)"){
        $("#expensed_amount").css("display","block");
    }
    else {
        $("#expensed_amount").css("display","none");
        $("#id_expenses_amount").val('')
    }
});

$("#id_organized_by_us").click(function(){
    if ($(this).is(':checked')){
        $("#organizer_name").css("display","block")
    }
    else {
        $("#organizer_name").css("display","none")
        $("#id_name_of_organizer").val('')
    }
});

