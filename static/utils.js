function turkGetParam( name, defaultValue ) {
    var regexS = "[\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var tmpURL = window.location.href;
    var results = regex.exec( tmpURL );
    if( results == null ) {
        return defaultValue;
    } else {
        return results[1];
    }
}

function getWorkerId() {
    if ( typeof(workerId) == 'undefined') {
        workerId = turkGetParam(
            'workerId', 
            'NONEb'+Math.floor(Math.random() * 10001)
        );
    }
    return workerId;
}

function isTurkPreview() {
    return (getWorkerId() == "NONE" && isOnTurk());
}

function getAssignmentId() {
    var assignmentId = turkGetParam( 'assignmentId', 'NONE' );
    return assignmentId;
}
function isOnTurk() {
    try {
        return ((window.location.host.indexOf('mturk')!=-1) || document.forms["mturk_form"] ||
            (top != self && window.parent.location.host.indexOf("mturk") != -1));
    } catch(err) {
        // insecure content trying to access https://turk probably, so say yes:
        return true
    }
}