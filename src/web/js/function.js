$(document).ready(function() {

    var download_bind = false
    var key = ""
    var test_response = `
`

    function init() {
        $("#do_submit").on("click", do_submit);
        $("input[type='download']").on("click", do_download);
    }

    function do_submit() {
        key = $("#key-input-entry").val();
        if (key != "") {
            $("#table-body").replaceWith(test_response);
            $("input[type='download']").on("click", do_download);
            if (!download_bind) {
                download_bind = true;
            }
        }
        return false
    }

    function do_download() {
        var id_obj = $(this).parent().parent().children()[0];
        var id = id_obj.innerHTML;
        alert(id);
    }

    init();
});
