//var timeoutFlag = false;

var correct = 0;
var incorrect = 0;




$(document).ready(function(){

    function finished(){
    $('#testtbl').fadeOut(100);
    $('#nextbtn').show();
};


    $('#testtbl').hide();
    $('#nextbtn').hide();

     $('#startbtn').click(function() {
        $('#testtbl').show();
        $('#startbtn').hide();
        //alert(correct + " " + incorrect);
        //$('#testtbl').delay(6000).finished();
        setTimeout(finished, 6000)
     });


    $('td').click(function(){
        if ($(this).hasClass("active")){
            $(this).removeClass("active");

            if ($(this).text().indexOf("a") != -1){
                correct = correct - 1;

                }
             else {
                incorrect = incorrect - 1;
                }
        } else {
            $(this).addClass("active");

            if ($(this).text().indexOf("a") != -1){
                correct = correct + 1;}
             else {
                incorrect = incorrect + 1;}

        }

        //$("#score").text(correct + " " + incorrect);
        $("#correct").val(correct);
        $("#incorrect").val(incorrect);


     });





});


