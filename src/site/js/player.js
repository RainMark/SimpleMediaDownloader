$(document).ready(function() {

    url = $('#song')[0].href;
    var audio = new Audio(url);

    audio.play();

    $('.trigger').click(function() {
        if (audio.paused == false) {
            audio.pause();
            $('.fa-play').show();
            $('.fa-pause').hide();
            $('.music-card').removeClass('playing');
        } else {
            audio.play();
            $('.fa-pause').show();
            $('.fa-play').hide();
            $('.music-card').addClass('playing');
        }
    });

});
