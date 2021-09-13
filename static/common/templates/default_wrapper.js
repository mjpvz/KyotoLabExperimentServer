$(document).ready(initialize);

function initialize() {
    console.log('Initialization of experiment wrapper')

    get_info()

    // get MTURK params from URL - this is a must
    document.worker_id = getWorkerId()
    document.assignmentID = turkGetParam('assignmentId', '');
    document.HITid = turkGetParam('hitId', '')
    document.onMturk = isOnTurk();

    document.continue = true
    document.url = 'https://labexperiment.cog.ist.i.kyoto-u.ac.jp/'

    workerDoneBefore() // make an async call. Only continue once this has finished
}

function get_info() {
    // get some basic info on the worker - if any of this is not available that's fine
    $.getJSON('https://ipapi.co/json/', function (data) {
        // console.log(data)
        document._ipdata = data
    });
    document._screen = {
        'availHeight': screen.availHeight,
        'availLeft': screen.availLeft,
        'availTop': screen.availTop,
        'availWidth': screen.availWidth,
        'colorDepth': screen.colorDepth,
        'height': screen.height,
        'pixelDepth': screen.pixelDepth,
        'width': screen.width,
        'orientation': screen.orientation.type
    }
    document._navigator = {
        'appVersion': navigator.appVersion,
        'language': navigator.language,
        'platform': navigator.platform,
        'userAgent': navigator.userAgent,
        'vendor': navigator.vendor,
    }
    document._size = {
        'w': innerWidth,
        'h': innerHeight
    }
}


function submit_data(data) {
    req = $.ajax({
        method: "POST",
        url: document.url + "data_submission",
        data: {
            'data': JSON.stringify({
                // Data on the user/machine
                'userData': {
                    'size': document._size,
                    'screen': document._screen,
                    'navigator': document._navigator,
                    'ipapidata': document._ipdata,
                },
                // These three are set in the experiment_wrapper.html 
                'experiment_name': document.experiment_name,
                'experiment_instance': document.experiment_instance,
                'condition': document.condition,
                // set through the mturk url params
                'worker_id': document.worker_id,
                'assignmentId': document.assignmentID,
                'HITid': document.HITid,
                // the actual data
                'payload': data
            }
            )
        }
    })
    req.done(function (response) {
        console.log("Data submitted succesfully")
        $('#assignmentId').val(document.assignmentID);
        $('#submitButton').click(); // auto click the mturk submit button.
    });

    req.fail(function (response) {
        console.log("Something has gone wrong..")
        // tryAgain(submit_data,1000)
    }
    );
}

function tryAgain(func, time) {
    window.setTimeout(func, time)
}

function start() {
    console.log("Starting..")
    if (isTurkPreview()) {
        show('preview_wrapper')
        document.continue = false
    }
    if (document.continue) {
        show('content_wrapper')
    }
}

function show(element) {
    // hide all elements
    $('main_element.show').removeClass('show').addClass('hidden');
    // switch the css display property of the provided element
    var ele = $(`#${element}`);
    ele.removeClass('hidden').addClass('show');
}

function workerDoneBefore() {
    if (!document.onMturk) {
        start() // if not on Mturk, no need to check/create worker instance
    } else {
        req = $.ajax({
            method: "GET",
            url: document.url + "workerCheck",
            data: {
                'worker_id': document.worker_id,
                'experiment_name': document.experiment_name,
            }
        })
        req.done(
            function (response) {
                console.log(response)
                if (document.sandbox) {
                    start() // if on Mturk sandbox, always continue
                    console.log("On MTURK start regardless")
                } else if (response == 'Found') {
                    console.log("Worker already done. Block")
                    show('already_done_wrapper')
                    document.continue = false
                } else {
                    start()
                }
            }
        );
    }
}

function turkGetParam(name, defaultValue) {
    var regexS = "[\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var tmpURL = window.location.href;
    var results = regex.exec(tmpURL);
    if (results == null) {
        return defaultValue;
    } else {
        return results[1];
    }
}

function getWorkerId() {
    return turkGetParam(
        'workerId',
        'NONEb' + Math.floor(Math.random() * 10001)
    );
}

function isTurkPreview() {
    return (getWorkerId() == "NONE" && isOnTurk());
}

function isOnTurk() {
    try {
        return ((window.location.host.indexOf('mturk') != -1) || document.forms["mturk_form"] ||
            (top != self && window.parent.location.host.indexOf("mturk") != -1));
    } catch (err) {
        // insecure content trying to access https://turk probably, so say yes:
        return true
    }
}







