//var timeoutFlag = false;

var correct = 0;
var incorrect = 0;

$(document).ready(function(){


    $('#testtbl').hide();

     $('#startbtn').click(function() {
        $('#testtbl').show();
        $('#startbtn').hide();
        //alert(correct + " " + incorrect);
        $('#testtbl').delay(6000).fadeOut(100);
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

$("#score").text(correct + " " + incorrect);
     });




});


