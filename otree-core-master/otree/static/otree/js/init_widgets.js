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
        $(document).on('change input', selector,setSliderValue);
    });
})();
