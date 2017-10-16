$(document).ready(function() {

    var xhr = new XMLHttpRequest();

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
            }
        };

        xhr.open("POST", "/api/v1/search", true);
        xhr.setRequestHeader('Content-Type',
                                      'application/x-www-form-urlencoded');
        xhr.send(encodeURI('key=' + key));
        return false
    }

    init();
});
