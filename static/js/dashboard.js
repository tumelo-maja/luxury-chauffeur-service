$(document).ready(function () {


    // Filter trips by button cliks
    $('#all-trips-button').click(() => {
        setTimeout(() => {
            console.log("Its ready now")
            $('#filter-button').on('click', function () {
                $('#filter-options').toggleClass('show');
            });

            $('#filter-options li').on('click', function () {
                filterTrips($(this).data('status'));
                $('#filter-options').removeClass('show');
                $('#filter-button .set-value').text($(this).text());

            });


            $(document).on('click', function (event) {
                if (!$(event.target).closest('#sort-button, #sort-options').length) {
                    $('#sort-options').removeClass('show');
                }
                if (!$(event.target).closest('#filter-button, #filter-options').length) {
                    $('#filter-options').removeClass('show');
                }
            });

            function filterTrips(status) {
                const trips = $('#trip_list .trip-item');
                let visibleTrips = 0;

                trips.each(function () {
                    const tripStatus = $(this).data('status');
                    if (status === 'all' || tripStatus === status) {
                        $(this).show();
                        visibleTrips++;
                    } else {
                        $(this).hide();
                    }
                });

                if (visibleTrips === 0) {
                    $('.empty-filter-list').text(`You do not have '${status.replace('_', ' ')}' trips`);
                    $('.empty-filter-list').show();
                } else {
                    $('.empty-filter-list').text("hidden");
                    $('.empty-filter-list').hide();
                }

            }

            filterTrips('all');

            ///

            htmx.on('htmx:afterSwap', (e) => {
                if ($(e.target).id === $('#trip_list').id) {
                    const selectedStatus = $('#filter-button .set-value').text().toLowerCase();
                    filterTrips(selectedStatus);
                    console.log("filter via Htmx has updated")

                }

            })

            $('#sort-button').on('click', function () {
                $('#sort-options').toggleClass('show');
                console.log("sort button cliked")
            });


            $('#sort-options li').on('click', function () {

                const [sortField, order] = $(this).data('sort').split('_');

                const fieldStr = $(this).find('span').text();
                sortTrips(sortField, order);
                $('#sort-options').removeClass('show');
                const iconType = order === 'asc' ? 'fa-sort-up' : 'fa-sort-down';
                console.log(`iconType: ${iconType}`);
                console.log(`order: ${order}`);
                console.log(`sortField: ${sortField}`);
                $('#sort-button').html(`<i class="fa-solid ${iconType}"></i> Sort: <span class="set-value">${fieldStr}</span>`);
            });

            // sort trip-list li elements basedOn field
            function sortTrips(sortField, order) {
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

            }

        }, 100);
    });

    setTimeout(() => {

        let ratingsTotal = 0;
        $('.rating-item').each(function (rateIndex) {

            const ratingValue = parseFloat($(this).find('.rating-value').text());
            // totalRatings = totalRatings
            ratingsTotal += ratingValue;

        });
        console.log(`This is the totalRatings: ${ratingsTotal}`);
        $('.ratings-total-value').text(ratingsTotal);


        // const ratingsTotal = parseFloat($('.ratings-total-value').text());
        $('.rating-item').each(function (rateIndex) {

            const ratingValue = parseFloat($(this).find('.rating-value').text());
            let newRatingFill = Math.round((ratingValue / ratingsTotal) * 100, 2);
            $(this).find('.rating-fill').css('width', newRatingFill + '%');
        });

    }, 200);



    console.log("Were working on ratings");

});
