$(document).ready(function () {

    htmx.on('htmx:afterSwap', (e) => {
        $('#listViewButton').on('click', setupTripsList);
        $('#calendarViewButton').on('click', setupTripsCalendar);
        $('#managerViewButton').on('click', setupTripsManager);
        $('.dash-item').on('click', setupDashButtons);

        updateRatingBars();       
    });

    /**
     * Update the width of rating bars based on their individual values
     * relative to the total count of ratings.
     */    
    function updateRatingBars() {
        const ratingsTotal = parseInt($('.ratings-total-count').text());

        $('.rating-item').each(function () {
            const ratingValue = parseFloat($(this).find('.rating-value').text());
            let newRatingFill = Math.round((ratingValue / ratingsTotal) * 100);
            $(this).find('.rating-fill').css('width', newRatingFill + '%');
        });
    }    

    $('#mobileDashMenu').change(function () {
        const selectedOption = $(this).find('option:selected')[0];
        htmx.trigger(selectedOption, 'click');

        if (selectedOption.id === 'calendarViewOption') {
            setupTripsCalendar();
        }
    });

    /**
     * Initialize the List Trips view.
     * Applies event listeners for filtering and sorting of trips.
     * Re-applies bindings after htmx has rendered html content.
     */
    function setupTripsList() {
        htmx.on('htmx:afterSwap', (e) => {

            // Toggles the filter dropdown list
            $('#filter-button').on('click', function () {
                $('#filter-options').toggleClass('show');
            });

            // Adds event listeners to filter options and runs filterTrips()
            $('#filter-options li').on('click', function () {
                $('#filter-options li').removeClass('current-filter');
                $(this).addClass('current-filter');
                filterTrips();
            });

            // Adds event listeners to collapse the filter and sort options for clicks outside these containers
            $(document).on('click', function (e) {
                if (!$(e.target).closest('#sort-button, #sort-options').length) {
                    $('#sort-options').removeClass('show');
                }
                if (!$(e.target).closest('#filter-button, #filter-options').length) {
                    $('#filter-options').removeClass('show');
                }
            });

            /**
             * Filter trips in the list based on the currently selected filter option.
             * Updates the DOM to show/hide trips accordingly.
             */
            function filterTrips() {
                const status = $('.current-filter').data('status');

                const trips = $('.trip-list .trip-item');
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

                $('#filter-options').removeClass('show');
                $('#filter-button .set-value').text($('.current-filter').text());
            }

            $('#sort-button').on('click', function () {
                $('#sort-options').toggleClass('show');
            });          

            // adds 'current-sort' class to the selected filter options - used in sortTrips()
            $('#sort-options li').on('click', function () {
                $('#sort-options li').removeClass('current-sort');
                $(this).addClass('current-sort');
                sortTrips();
            });

            /**
             * Sort trips in the list based on the selected sort option.
             * Updates DOM to display sorted trips.
             */
            function sortTrips() {
                const [sortField, order] = $('.current-sort').data('sort').split('_');
                const trips = $('.trip-list .trip-item');

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

                $('.trip-list ul').html(trips);

                const fieldStr = $('.current-sort').find('span').text();
                $('#sort-options').removeClass('show');
                const iconType = order === 'asc' ? 'fa-sort-up' : 'fa-sort-down';
                $('#sort-button').html(`<i class="fa-solid ${iconType}"></i> Sort: <span class="set-value">${fieldStr}</span>`);
            }
        });
    }

    /**
     * Initialize the Calendar view.
     * Fetches trips for the current month and renders them in a calendar grid.
     * Displays current user's trips in the calendar
     * Allows navigation between months and trip creation for passenger users.
     */
    function setupTripsCalendar() {

        const userType = $('#user-name').data('profile-type')
        htmx.on('htmx:afterSwap', (e) => {

            const monthYear = $('#monthYear');
            const datesElement = $('#dates');
            const prevBtn = $('#prevBtn');
            const nextBtn = $('#nextBtn');
            let currentDate = new Date();

            /**
             * Fetch trips for a given year and month.
             * Returns a list of trip objects from the backend.
             */            
            async function getMonthlyTrips(year, month) {
                try {
                    const response = await fetch(`/trips/calendar/subsets/?year=${year}&month=${month}`);
                    const data = await response.json();
                    return data.trips || [];
                } catch (error) {
                    return [];
                }
            }

            /**
             * Render and update the calendar UI elements for the displayed month.
             * Displays trip counts for each day of the month.
             */            
            async function  updateCalendar() {
                const currentYear = currentDate.getFullYear();
                const currentMonth = currentDate.getMonth();

                const firstDay = new Date(currentYear, currentMonth, 0);
                const lastDay = new Date(currentYear, currentMonth + 1, 0);

                const totalDays = lastDay.getDate();
                const firstDayIndex = firstDay.getDay();
                const lastDayIndex = lastDay.getDay();

                const monthYearString = currentDate.toLocaleString(
                    'default', { month: 'long', year: 'numeric' });

                monthYear.text(monthYearString);

                const trips = await getMonthlyTrips(currentYear, currentMonth + 1);
                let datesHTML = '';
                for (let i = firstDayIndex; i > 0; i--) {
                    const prevDate = new Date(currentYear, currentMonth, 1 - i);
                    datesHTML += `<div class="date-wrapper"><div class="cal-date inactive">${prevDate.getDate()}</div></div>`
                }

                for (let i = 1; i <= totalDays; i++) {
                    const date = new Date(currentYear, currentMonth, i);
                    let todayDate = new Date();

                    let clickedDate = new Date(date);
                    clickedDate.setHours(todayDate.getHours() + 1, todayDate.getMinutes() + 30);
                    const datetimeNow = clickedDate.toISOString().slice(0, 16);

                    todayDate.setHours(0, 0, 0, 0);
                    const activeClass = date.toDateString() === todayDate.toDateString() ? 'active' : '';
                    const pastDays = date < todayDate ? 'past-days' : '';
                    const dateString = date.toLocaleDateString();

                    let tripCount = trips.filter(trip => trip.travel_date === dateString).length;
                    let tripCountStr = tripCount > 9 ? '9+' : `${tripCount}`;

                    const tripElement = `<div class="day-trips"><span class= "day-trip-count">${tripCountStr}</span> <i class="fa-solid fa-car-rear"></i></div>`;

                    // add htmx attributes for trip request - passenger users only
                    let htmxCreateTrip = '';
                    if (date >= todayDate && userType === 'passenger') {
                        htmxCreateTrip = `hx-get="/trips/request/?datetime=${datetimeNow}" hx-target="#baseDialog"`;
                    }

                    datesHTML += `<div class="date-wrapper">
                                    <div class="cal-date ${activeClass} ${pastDays}"${htmxCreateTrip}>${i}</div>
                                    ${tripCount > 0 ? tripElement : ''}
                                  </div>`
                }

                for (let i = 1; i <= 7 - lastDayIndex; i++) {
                    const nextDate = new Date(currentYear, currentMonth + 1, i);
                    datesHTML += `<div class="date-wrapper"><div class="cal-date inactive">${nextDate.getDate()}</div></div>`
                }

                datesElement.html(datesHTML);

                // re-adds htmx event listeners for htmx attributes
                $('.cal-date').each(function () {
                    htmx.process(this);
                })
            }

            // Handles navigating to the previous month and runs updateCalendar()
            $(prevBtn).click(() => {
                currentDate.setMonth(currentDate.getMonth() - 1);
                updateCalendar();
            })

            // Handles navigating to the next month and runs updateCalendar()
            $(nextBtn).click(() => {
                currentDate.setMonth(currentDate.getMonth() + 1);
                updateCalendar();
            })

            updateCalendar();
        });
    }


    // Setup trips manager view  - Dashsetup
    /**
     * Initialize the Trips Manager view.
     * Adds event listeners for tab navigation.
     */
    function setupTripsManager() {
        htmx.on('htmx:afterSwap', (e) => {
            $('.manager-all .nav-link').on('click', function () {
                $('.manager-all .nav-link').removeClass('active');
                $(this).addClass('active');
            });

        });
    }

    // handle dashboard button clicks - dashsetup
    /**
     * Highlight the clicked dashboard items clicked.
     */    
    function setupDashButtons() {
        $('.dash-item').removeClass('selected');
        $(this).addClass('selected');
    }

});
