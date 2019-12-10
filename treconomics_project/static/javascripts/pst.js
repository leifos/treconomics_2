//var timeoutFlag = false;

var correct = 0;
var incorrect = 0;

$(document).ready(function(){
    var timeoutHandle;
    function countdown(minutes, seconds) {
        function tick() {
            var counter = document.getElementById("timer");
            counter.innerHTML =
                minutes.toString() + ":" + (seconds < 10 ? "0" : "") + String(seconds);
            seconds--;
            if (seconds >= 0) {
                timeoutHandle = setTimeout(tick, 1000);
            } else {
                if (minutes >= 1) {
                    // countdown(mins-1);   never reach “00″ issue solved:Contributed by Victor Streithorst
                    setTimeout(function () {
                        countdown(minutes - 1, 59);
                    }, 1000);
                }
            }
        }
        tick();
    };

    function finished(){
    $('#pst_test').fadeOut(100);
    $('#nextbtn').show();
    $('#finished').show();

    alert("Times up for completing the perceptual speed test - click next to continue.")
    };

    $('#finished').hide();
    $('#pst_test').hide();
    $('#nextbtn').hide();
    $('#pst1').hide();
    $('#pst2').hide();
    $('#pst3').hide();
    $('#pst4').hide();

 $('#btn1').click(function() {
    $('#pst1').show();
    $('#pst2').hide();
    $('#pst3').hide();
    $('#pst4').hide();
            $('#btn1').css({"background-color":"grey"});
            $('#btn2').css({"background-color":"white"});
            $('#btn3').css({"background-color":"white"});
            $('#btn4').css({"background-color":"white"});

 });

 $('#btn2').click(function() {
    $('#pst2').show();
    $('#pst1').hide();
    $('#pst3').hide();
    $('#pst4').hide();
             $('#btn1').css({"background-color":"white"});
            $('#btn2').css({"background-color":"grey"});
            $('#btn3').css({"background-color":"white"});
            $('#btn4').css({"background-color":"white"});
 });

 $('#btn3').click(function() {
    $('#pst2').hide();
    $('#pst1').hide();
    $('#pst3').show();
    $('#pst4').hide();
            $('#btn1').css({"background-color":"white"});
            $('#btn2').css({"background-color":"white"});
            $('#btn3').css({"background-color":"grey"});
            $('#btn4').css({"background-color":"white"});
 });


 $('#btn4').click(function() {
    $('#pst2').hide();
    $('#pst1').hide();
    $('#pst3').hide();
    $('#pst4').show();
            $('#btn1').css({"background-color":"white"});
            $('#btn2').css({"background-color":"white"});
            $('#btn3').css({"background-color":"white"});
            $('#btn4').css({"background-color":"grey"});
 });


     $('#startbtn').click(function() {
        $('#pst_test').show();
        $('#pst1').show();
        $('#btn1').css({"background-color":"grey"});
        $('#startbtn').hide();
        $('#pst_instructions').hide();
        countdown(2, 0);
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


