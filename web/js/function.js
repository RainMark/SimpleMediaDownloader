$(document).ready(function() {

    var download_bind = false
    var key = ""
    var test_response = `
      <div class="list" id="media-list">
        <table class="u-full-width">
          <thead>
            <th>ID</th>
            <th>Name</th>
            <th>Source</th>
            <th>Type</th>
            <th>Download</th>
          </thead>
          <tbody>
            <tr>
              <td>MH77</td>
              <td>九张机 (国语) - 叶炫清</td>
              <td>QQ</td>
              <td>MPEG3</td>
              <td>
                <input class="button" type="download" value="Download">
              </td>
            </tr>

            <tr>
              <td>GD54</td>
              <td>越过山丘 (Live) - 李雅</td>
              <td>QQ</td>
              <td>MPEG3</td>
              <td>
                <input class="button" type="download" value="Download">
              </td>
            </tr>

            <tr>
              <td>GS54</td>
              <td>从前慢 (Live) - 叶炫清</td>
              <td>QQ</td>
              <td>MPEG3</td>
              <td>
                <input class="button" type="download" value="Download">
              </td>
            </tr>

            <tr>
              <td>MS90</td>
              <td>紫 (Live) - 郭沁</td>
              <td>QQ</td>
              <td>MPEG3</td>
              <td>
                <input class="button" type="download" value="Download">
              </td>
            </tr>

            <tr>
              <td>SC90</td>
              <td>想自由 (Live) - 叶炫清</td>
              <td>QQ</td>
              <td>MPEG3</td>
              <td>
                <input class="button" type="download" value="Download">
              </td>
            </tr>

          </tbody>
        </table>
      </div>
`

    function init() {
        $("#do_submit").on("click", do_submit);
        $("input[type='download']").on("click", do_download);
    }

    function do_submit() {
        key = $("#key-input-entry").val();
        if (key != "") {
            $("#media-list").replaceWith(test_response);
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
