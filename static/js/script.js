$(document).ready(function () {

    $(".dropdown-head").click(function () {
        $(".arrow-icon").toggleClass('rotate');
        $(".dropdown-body").toggleClass('hidden-item');
    });

    console.log("hello world - Yes");

    // Handle message displays
    const messages = $('.message');

    messages.each(function (index) {
        const message = $(this);

        setTimeout(function () {
            message.addClass('show');
        }, 200 + index * 300);

        setTimeout(function () {
            message.removeClass('show');
        }, 6000 + index * 300);
    });


    $('.close-btn').click(function () {
        $(this).closest('.message').removeClass('show');
    });

$(document).ready(function () {
    const $slideElements = $('.service-item');
    const $buttonElements = $('.btn-item');
    let currentSlide = 1;

    // Manual carousel navigation
    const manualNav = function (manual) {
        $slideElements.removeClass('active');
        $buttonElements.removeClass('active');

        $($slideElements[manual]).addClass('active');
        $($buttonElements[manual]).addClass('active');
    }

    // Handling button click
    $buttonElements.each(function (i) {
        $(this).on('click', function () {
            manualNav(i);
            currentSlide = i;
        });
    });

    // Carousel autoplay
    const repeat = function () {
        let i = 1;

        const repeater = function () {
            setTimeout(function () {
                $slideElements.removeClass('active');
                $buttonElements.removeClass('active');

                $($slideElements[i]).addClass('active');
                $($buttonElements[i]).addClass('active');
                i++;

                if (i == $slideElements.length) {
                    i = 0;
                }

                if (i < $slideElements.length) {
                    repeater();
                }
            }, 5000);
        }

        repeater();
    }

    repeat();
});


});