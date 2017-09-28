$(document).ready(function() {

    var download_bind = false
    var key = ""
    var ajax_request = new XMLHttpRequest()

    function init() {
        $("#do_submit").on("click", do_submit);
        $("input[type='download']").on("click", do_download);
    }

    function do_submit() {
        key = $("#key-input-entry").val();
        if (key != "") {
            if (!download_bind) {
                download_bind = true;
            }
            ajax_request.onreadystatechange = ajax_request_callback;
            ajax_request.open("POST", "http://localhost/api/v1/search", true);
            ajax_request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            ajax_request.send(encodeURI('key=' + key));
        }
        return false
    }

    function do_download() {
        var id_obj = $(this).parent().parent().children()[0];
        var id = id_obj.innerHTML;
        alert(id);
    }

    function ajax_request_callback() {
        if (ajax_request.readyState == 4) {
            if (ajax_request.status == 200) {
                $("#table-body").replaceWith(ajax_request.responseText);
                $("input[type='download']").on("click", do_download);
            }
        }
    }

    init();
});
