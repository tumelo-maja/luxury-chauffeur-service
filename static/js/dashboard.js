$(document).ready(function () {


    // Filter trips by button cliks
    $('#all-trips-button').click(() => {
        setTimeout(() => {

            $('#filter-button').on('click', function () {
                $('#filter-options').toggleClass('show');
            });

            $('#filter-options li').on('click', function () {
                $('#filter-options li').removeClass('current-filter');
                $(this).addClass('current-filter');

                filterTrips();
            });


            $(document).on('click', function (event) {
                if (!$(event.target).closest('#sort-button, #sort-options').length) {
                    $('#sort-options').removeClass('show');
                }
                if (!$(event.target).closest('#filter-button, #filter-options').length) {
                    $('#filter-options').removeClass('show');
                }
            });


            function filterTrips() {
                const status = $('.current-filter').data('status');

                const trips = $('#trip_list .trip-item');
                let visibleTrips = 0;

                trips.each(function (trip_idx) {
                    const tripStatus = $(this).data('status');
                    if (status === 'all' || tripStatus === status) {
                        $(this).show();
                        visibleTrips++;
                        $(this).addClass('filtered');
                    } else {
                        $(this).hide();
                        $(this).removeClass('filtered');
                    }
                });

                if (visibleTrips === 0) {
                    $('.empty-filter-list').text(`You do not have '${status.replace('_', ' ')}' trips`);
                    $('.empty-filter-list').show();
                } else {
                    $('.empty-filter-list').text("hidden");
                    $('.empty-filter-list').hide();

                }

                $('#trip_list .filtered').first().click();

                $('#filter-options').removeClass('show');
                $('#filter-button .set-value').text($('.current-filter').text());
            }

            ///
            htmx.on('htmx:beforeSwap', (e) => {
                if ($(e.target).id === $('#trip_list').id && !e.detail.xhr.response) {
                    detailID = $('#tripDetail').data('id')
                    $(`#trip_list #${detailID}`).click();
                    filterTrips();
                    sortTrips();
                    addTripItemListener();
                }
            })

            $('#sort-options li').on('click', function () {
                $('#sort-options li').removeClass('current-sort');
                $(this).addClass('current-sort');
                sortTrips();
            });

            // sort trip-list li elements basedOn field
            function sortTrips() {
                const [sortField, order] = $('.current-sort').data('sort').split('_');
                const trips = $('#trip_list .trip-item');


                trips.sort(function (a, b) {
                    const aValue = $(a).data(sortField);
                    const bValue = $(b).data(sortField);

                    if (sortField === 'status') {
                        return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
                    }

                    if (order === 'asc') {
                        return aValue - bValue;
                    } else {
                        return bValue - aValue;
                    }
                });

                $('#trip_list ol').html(trips);
                $('#trip_list .filtered').first().click();

                const fieldStr = $('.current-sort').find('span').text();
                $('#sort-options').removeClass('show');
                const iconType = order === 'asc' ? 'fa-sort-up' : 'fa-sort-down';
                $('#sort-button').html(`<i class="fa-solid ${iconType}"></i> Sort: <span class="set-value">${fieldStr}</span>`);

            }

        }, 100);
    });

    setTimeout(() => {

        $('.rating-item').each(function (rateIndex) {
            const ratingValue = parseFloat($(this).find('.rating-value').text());
            const ratingsTotal = parseInt($('.ratings-total-count').text());
            let newRatingFill = Math.round((ratingValue / ratingsTotal) * 100, 2);
            $(this).find('.rating-fill').css('width', newRatingFill + '%');
        });

    }, 200);


    function addTripItemListener() {
        $('.trip-item').on('click', function () {
            $('.trip-item').removeClass('current-detail');
            $(this).addClass('current-detail');
        });
    }


    // admin panel interactive elements
    $('#admin-all-button').click(() => {
        console.log("admin button pushed");
        setTimeout(() => {
            $('.admin-all .nav-link').on('click', function () {
                $('.admin-all .nav-link').removeClass('active');
                $(this).addClass('active');
                console.log("Nav item clicked");
            });

        }, 100);
    });

});
