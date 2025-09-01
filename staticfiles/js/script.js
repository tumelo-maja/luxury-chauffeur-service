$(document).ready(function () {

    /**
     * Toggles dropdown visibility and arrow rotation
     * when the dropdown header is clicked.
     */    
    $(".dropdown-head").click(function () {
        $(".arrow-icon").toggleClass('rotate');
        $(".dropdown-body").toggleClass('hidden-item');
    });

    /**
     * Handles display of messages:
     * - Fade in messages sequentially.
     * - Auto-hide messages after a few seconds.
     */    
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

    /**
     * Close a message display when its close button is clicked.
     */
    $('.close-btn').click(function () {
        $(this).closest('.message').removeClass('show');
    });

    // Hero carousel elements
    const $slideElements = $('.hero-item');
    const $buttonElements = $('.btn-item');
    let currentSlide = 1;

    // Manual carousel navigation
    /**
     * Navigate to a specific carousel slide.
     * @param {number} manual - The index of the slide to show.
     */    
    const manualNav = function (manual) {
        $slideElements.removeClass('active');
        $slideElements.addClass('hidden-item');
        $buttonElements.removeClass('active');

        $($slideElements[manual]).addClass('active');
        $($slideElements[manual]).removeClass('hidden-item');
        $($buttonElements[manual]).addClass('active');
    }

    /**
     * Handle carousel navigation button clicks.
     * Updates the current slide index.
     */    
    $buttonElements.each(function (i) {
        $(this).on('click', function () {
            manualNav(i);
            currentSlide = i;
        });
    });

    // Carousel autoplay
    /**
     * Handles auto play of carousel slides.
     */    
    const repeat = function () {
        let i = 1;

        const repeater = function () {
            setTimeout(function () {
                $slideElements.removeClass('active');
                $slideElements.addClass('hidden-item');
                $buttonElements.removeClass('active');

                $($slideElements[i]).removeClass('hidden-item');
                $($slideElements[i]).addClass('active');
                $($slideElements[i]).show();
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

    /**
     * Initialize the Flatpickr datetime picker for trip inputs.
     */    
    function initializeFlatpicker() {
        flatpickr(".trip_datetime", {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            minuteIncrement: 15,
            time_24hr: true,
        });
    }

    initializeFlatpicker();

    // initialize Bootstrap modal - #baseModal
    const modal = new bootstrap.Modal($('#baseModal'));
    /**
     * Show modal after HTMX swap into #baseDialog
     * and reinitialize Flatpickr inside the modal.
     */    
    htmx.on('htmx:afterSwap', (e) => {
        if (e.detail.target.id === 'baseDialog') {
            modal.show();
            initializeFlatpicker();
        }
        console.log("all before swap:")
        console.log(e.detail.xhr.status)
    })

    /**
     * Show modal after HTMX swap into #baseDialog
     * and reinitialize Flatpickr inside the modal.
     */    
    htmx.on('htmx:beforeSwap', (e) => {
        // console.log
        console.log("all before swap:")
        console.log(e.detail.xhr.status)
        if (e.detail.xhr.status === 302) {
            modal.hide();
        }
    })

    /**
     * Clears the modal content when it is hidden.
     */    
    htmx.on('hidden:bs.modal', (e) => {
        document.getElementById('baseDialog').innerHTML = '';
    })

    // navbar toggle elements
    const $mainHead = $('.header-main');
    const $sectionWrapper = $('.section-wrapper');

    /**
     * Toggle navbar state on navbar-toggler clicks.
     */    
    $('.navbar-toggler').click(function () {
        $mainHead.toggleClass('active');
        $sectionWrapper.toggleClass('active');
        console.log("navbar toggled");
    });
});