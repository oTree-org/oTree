function makeReconnectingWebSocket(path) {
    // https://github.com/pladaria/reconnecting-websocket/issues/91#issuecomment-431244323
    var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    var ws_path = `${ws_scheme}://${window.location.host}${path}`;
    var socket = new ReconnectingWebSocket(ws_path);
    socket.onclose = function (e) {
        if (e.code === 1011) {
            // this may or may not exist in child pages.
            var serverErrorDiv = document.getElementById("websocket-server-error");
            if (serverErrorDiv) {
                // better to put the message here rather than the div, otherwise it's confusing when
                // you do "view source" and there's an error message.
                serverErrorDiv.innerText = "Server error. Check the server logs or Sentry.";
                serverErrorDiv.style.visibility = "visible";
            }
        }
    };
    return socket;
}

(function () {
    'use strict';

    $(document).ready(function () {
        var selector = '[data-slider] input[type="range"]';
        var setSliderValue = function () {
            var $input = $(this),
                $slider = $input.closest('[data-slider]'),
                $valueTarget = $slider.find('[data-slider-value]'),
                value = $input.val();
            $valueTarget.text(value);
        };

        $(selector).each(setSliderValue);
        $(document).on('change input', selector, setSliderValue);
        // block the user from spamming the next button which can make congestion
        // problems worse.
        // i can't use $('.otree-btn-next').click()
        // because disabling the button inside the handler interferes with form
        // submission.
        $('#form').submit(function () {
            $('.otree-btn-next').each(function () {
                var nextButton = this;
                var originalState = nextButton.disabled;
                nextButton.disabled = true;
                setTimeout(function () {
                    // restore original state.
                    // it's possible the button was disabled in the first place?
                    nextButton.disabled = originalState;
                }, 15000);
            });
        });
    });
})();
