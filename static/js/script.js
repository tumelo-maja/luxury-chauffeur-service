$(document).ready(function () {

    $(".dropdown-head").click(function () {
        $(".arrow-icon").toggleClass('rotate');
        $(".dropdown-body").toggleClass('hidden-item');
    });

    console.log("hello world");

    // Handle message displays
    $(document).ready(function () {
        const messages = $('.message');

        messages.each(function (index) {
            const message = $(this);

            // Show the message with a delay, and hide after 6 seconds.
            setTimeout(function () {
                message.addClass('show'); // Show the message
            }, 200 + index * 300); // Add a delay between messages

            setTimeout(function () {
                message.removeClass('show'); // Hide the message
            }, 6000 + index * 300); // Keep the message visible for 6 seconds
        });

        // Close a message when the close button is clicked
        $('.close-btn').click(function () {
            $(this).closest('.message').removeClass('show');
        });
    });

});