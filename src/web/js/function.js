$(document).ready(function() {

    var SITE = 'http://127.0.0.1';
    var file_name = '';
    var xhr = new XMLHttpRequest();
    var lock = false;
    var progressbar = null;

    function init() {
        $("#do_submit").on("click", do_submit);
    }

    function do_submit() {
        var key = $("#key-input-entry").val();
        if (key == "") {
            return false;
        }

        xhr.onreadystatechange = function() {
            state = xhr.readyState;
            status = xhr.status;
            if (4 == state && 200 == status) {
                $("#table-body").replaceWith(xhr.responseText);
                $("input[type='download']").on("click", do_download);
            }
        };

        xhr.open("POST", SITE + "/api/v1/search", true);
        xhr.setRequestHeader('Content-Type',
                                      'application/x-www-form-urlencoded');
        xhr.responseType = 'text';
        xhr.send(encodeURI('key=' + key));
        return false
    }

    function do_download() {
        var id_obj = $(this).parent().parent().children()[0];
        var name_obj = $(this).parent().parent().children()[1];
        var id = id_obj.innerHTML;
        file_name = name_obj.innerHTML;

        if (lock) {
            return false;
        } else {
            lock  = true;
        }
        _id = 'progress' + id;
        $(this).replaceWith('<div class=\"progressbar\" id=\"' + _id + '\"></div>');
        progressbar = new ProgressBar.Line('#' + _id, {
            strokeWidth: 4,
            easing: 'easeInOut',
            duration: 1400,
            color: '#33C3F0',
            trailColor: '#eee',
            trailWidth: 1,
            svgStyle: {width: '100%', height: '100%'}
        });

        xhr.open("POST", SITE + "/api/v1/download", true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.responseType = 'blob';
        xhr.onprogress = function(evt) {
            if (evt.lengthComputable) {
                progressbar.animate(evt.loaded / evt.total);
            }
        };
        xhr.onloadend = function(evt) {
            progressbar.animate(1.0);
            lock = false;
        };
        xhr.onreadystatechange = function() {
            state = xhr.readyState;
            status = xhr.status;
            if (4 == state && 200 == status && '' != file_name) {
                download(xhr.response, file_name, 'audio/mpeg');
            }
        };

        xhr.send(encodeURI('id=' + id));
        return false
    }

    init();
});
