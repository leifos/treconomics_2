$(document).ready(function(){
    var isJSEnabled = true;
    var isResolutionOkay = false;
    var isAdblockerDisabled = false;

    var width = screen.width;
    var height = screen.height;

    /* If this is executed, JS must be enabled, so just hide the text saying it isn't! */
    $('#registrationWarning-javascript').hide();

    /* Check the resolution. */
    if ((width !== undefined || height !== undefined) && (width < 1024 || height < 768)) {
        $('#registrationWarning-resolution').show();
    }
    else {
        isResolutionOkay = true;
    }

    /* Check for an adblocker. */
    var loadedElement = $('#HILooYTq0FOFkFI');
    
    if (!loadedElement.length) {  /* Does the element exist? */
        $('#registrationWarning-adblockers').show();
    }
    else {
        isAdblockerDisabled = true;
    }

    /* Everything okay? */
    if (isJSEnabled && isResolutionOkay && isAdblockerDisabled) {
        $('#crowdSourceRegistrationWarningArea').hide();
        $('#crowdSourceRegistrationArea').show();
    }
});