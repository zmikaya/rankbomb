// keep the form value the same as the user selection
$("#selection").val($("#compType").text())
$("li").click(function(){
    $("#selection").val($("#compType").text());
})

