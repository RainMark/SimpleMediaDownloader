$(document).ready(function() {

    var file_name = '';
    var ajax_request = new XMLHttpRequest();

    function init() {
        $("#do_submit").on("click", do_submit);
    }

    function do_submit() {
        var key = $("#key-input-entry").val();
        if (key == "") {
            return false;
        }

        ajax_request.onreadystatechange = function() {
            state = ajax_request.readyState;
            status = ajax_request.status;
            if (4 == state && 200 == status) {
                $("#table-body").replaceWith(ajax_request.responseText);
                $("input[type='download']").on("click", do_download);
            }
        };

        ajax_request.open("POST", "/api/v1/search", true);
        ajax_request.setRequestHeader('Content-Type',
                                      'application/x-www-form-urlencoded');
        ajax_request.responseType = 'text';
        ajax_request.send(encodeURI('key=' + key));
        return false
    }

    function do_download() {
        var id_obj = $(this).parent().parent().children()[0];
        var name_obj = $(this).parent().parent().children()[1];
        var id = id_obj.innerHTML;
        file_name = name_obj.innerHTML;

        ajax_request.onreadystatechange = function() {
            state = ajax_request.readyState;
            status = ajax_request.status;
            if (4 == state && 200 == status && '' != file_name) {
                download(ajax_request.response, file_name, 'audio/mpeg');
            }
        };

        ajax_request.open("POST", "/api/v1/download", true);
        ajax_request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        ajax_request.responseType = 'blob';
        ajax_request.send(encodeURI('id=' + id));
        return false
    }

    init();
});
