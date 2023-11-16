<script>
document.addEventListener("DOMContentLoaded", function () {
    // Get all input fields with the 'data-jdp' and 'data-jdp-only-time' attributes
    var dateInput = document.getElementById('dateInput');
    var timeInput = document.getElementById('timeInput');

    // Initialize Jalali Datepicker for the date input
    if (dateInput) {
        jalaliDatepicker.startWatch({
            input: dateInput, // Specify the date input field
            // minDate: "attr",
            // maxDate: "attr",
            time: false, // Date-only configuration
            date: true, // Enable date input
            // Other configuration options here
        });
    }

    // Initialize Jalali Datepicker for the time input
    if (timeInput) {
        jalaliDatepicker.startWatch({
            input: timeInput, // Specify the time input field
        });
    }
});
</script>