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

        // handle the ratings section
        // const ratingsTotal = parseFloat($('.ratings-total-value').text());
        // const ratingFill = $('.rating-fill').css('width');
        // const ratingValue = parseFloat($('#rating-value-5').text());
        // let newRatingFill = Math.round((ratingValue / ratingsTotal) * 100, 2);

        // console.log(`ratingsTotal: ${ratingsTotal}`);
        // console.log(`ratingFill: ${ratingFill}`);
        // console.log(`ratingValue: ${ratingValue}`);
        // console.log(`newRatingFill: ${newRatingFill}`);
        // $('.rating-fill').css('width', newRatingFill + '%');
        // console.log(`after change: ${$('.rating-fill').css('width')}`);

        const ratingsTotal = parseFloat($('.ratings-total-value').text());
        $('.rating-item').each(function(rateIndex) {

            const ratingValue = parseFloat($(this).find('.rating-value').text());
            console.log(this)
            console.log(`ratingValue ${rateIndex}: ${ratingValue}`)
            let newRatingFill = Math.round((ratingValue / ratingsTotal) * 100, 2);
            $(this).find('.rating-fill').css('width', newRatingFill + '%');
            console.log(`after change: ${$('.rating-fill').css('width')}`);
        });


        function updateMovesRemaining(moveType) {

            // const attributeValue = parseFloat(getComputedStyle(object).getPropertyValue(attribute));

            const ratingItem = $('.rating-bar');
            const ratingFill = $('.rating-fill');
            const ratingValue = $('.rating-value-5');

            let newRatingFill = Math.round(ratingValue / ratingsTotal, 2) * 100;
            ratingFill.style.width = newRatingFill + '%';
            // const ratingItem = Math.round(100 / gameMode.maximumMoves, 2);
            userMoves = movesNumberElement.textContent;

            let currentBarwidth = (getCssStyleValue(movesBar, 'width') / getCssStyleValue(gameMoves, 'width')) * 100;
            let newBarwidth = 0;
            if (moveType === 'forward') {
                newBarwidth = currentBarwidth - widthIncrements;
                --userMoves;
            } else {
                newBarwidth = currentBarwidth + widthIncrements;
                ++userMoves;
            }

            movesNumberElement.textContent = userMoves;
            movesBar.style.width = newBarwidth + '%';
        }

    }, 200);



    console.log("Were working on ratings");

});
