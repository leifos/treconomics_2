//var timeoutFlag = false;

var correct = 0;
var incorrect = 0;

$(document).ready(function(){

    function finished(){
    $('#pst_test').fadeOut(100);
    $('#nextbtn').show();
    };

    $('#pst_test').hide();
    $('#nextbtn').hide();
    $('#pst1').hide();
    $('#pst2').hide();


 $('#btn1').click(function() {
    $('#pst1').show();
    $('#pst2').hide();

 });

 $('#btn2').click(function() {
    $('#pst2').show();
    $('#pst1').hide();

 });


     $('#startbtn').click(function() {
        $('#pst_test').show();
        $('#pst1').show()
        $('#startbtn').hide();
        $('#pst_instructions').hide();


        setTimeout(finished, 30000)
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


