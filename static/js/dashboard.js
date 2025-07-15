$(document).ready(function () {


    // Filter trips by button cliks
    $('#all-trips-button').click(() => {
        setTimeout(() => {
            console.log("Its ready now")

            $('#status-filter').on('change', function () {
                filterTrips($(this).val());
            });

            function filterTrips(status) {
                let visibleTrips = 0;

                $('#trip_list .trip-item').each(function () {
                    const tripStatus = $(this).data('status');
                    if (status === 'all' || tripStatus === status) {
                        $(this).show();
                        visibleTrips++;
                    } else {
                        $(this).hide();
                    }
                });
                console.log("Its all changed.")

                if (visibleTrips === 0) {
                    $('.empty-filter-list').text(`You do not have '${status.replace('_', ' ')}' trips`);
                    $('.empty-filter-list').show();
                } else {
                    $('.empty-filter-list').text("hidden");
                    $('.empty-filter-list').hide();
                }

            }

            htmx.on('htmx:afterSwap', (e) => {
                if ($(e.target).id === $('#trip_list').id) {
                    const selectedStatus = $('#status-filter').val();
                    filterTrips(selectedStatus);
                    console.log("filter via Htmx has updated")

                }

            })

            // sort trip-list by fields
            $('#field-sort').on('change', function () {
                sortTrips($(this).val());
                console.log('iterms sorted');
            });

            function sortTrips(sortValue) {

                const [sortField, order] = sortValue.split('_');

                const trips = $('#trip_list .trip-item');

                console.log('Sorrt ready');
                console.log(`sortField: ${sortField}`);
                console.log(`order: ${order}`);

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
});
