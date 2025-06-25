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

});