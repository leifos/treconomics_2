//var timeoutFlag = false;

var correct = 0;
var incorrect = 0;

$(document).ready(function(){

    function finished(){
    $('#pst_test').fadeOut(100);
    $('#nextbtn').show();
    alert("Times up for completing the perceptual speed test - click next to continue.")
    };

    $('#pst_test').hide();
    $('#nextbtn').hide();
    $('#pst1').hide();
    $('#pst2').hide();
    $('#pst3').hide();

 $('#btn1').click(function() {
    $('#pst1').show();
    $('#pst2').hide();
    $('#pst3').hide();
            $('#btn1').hide();
            $('#btn2').show();
            $('#btn3').show();

 });

 $('#btn2').click(function() {
    $('#pst2').show();
    $('#pst1').hide();
    $('#pst3').hide();
            $('#btn2').hide();
             $('#btn1').show();
            $('#btn3').show();
 });

 $('#btn3').click(function() {
    $('#pst2').hide();
    $('#pst1').hide();
    $('#pst3').show();
            $('#btn3').hide();
             $('#btn2').show();
            $('#btn1').show();
 });



     $('#startbtn').click(function() {
        $('#pst_test').show();
        $('#pst1').show();
        $('#btn1').hide();
        $('#startbtn').hide();
        $('#pst_instructions').hide();


        setTimeout(finished, 120000)
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


