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

    const $slideElements = $('.hero-item');
    const $buttonElements = $('.btn-item');
    let currentSlide = 1;

    // Manual carousel navigation
    const manualNav = function (manual) {
        $slideElements.removeClass('active');
        $slideElements.addClass('hidden-item');
        $buttonElements.removeClass('active');

        // $($slideElements[manual]).toggleClass('active hidden-item');
        $($slideElements[manual]).addClass('active');
        $($slideElements[manual]).removeClass('hidden-item');
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
                $slideElements.addClass('hidden-item');
                $buttonElements.removeClass('active');

                // $($slideElements[i]).toggleClass('active hidden-item');
                $($slideElements[i]).removeClass('hidden-item');
                $($slideElements[i]).addClass('active');
                $($slideElements[i]).show();
                // $($slideElements[i]).removeClass('hidden-item');
                $($buttonElements[i]).addClass('active');
                i++;

                if (i == $slideElements.length) {
                    i = 0;
                }

                if (i < $slideElements.length) {
                    repeater();
                }
            }, 4000);
        }

        repeater();
    }

    repeat();
});