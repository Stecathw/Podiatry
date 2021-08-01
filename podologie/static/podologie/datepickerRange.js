$(function() {
    var dateFormat = "dd-mm-yy",
    from = $( "#from" ).datepicker({
        minDate: "+1d",
        maxDate: "+1y",
        changeMonth: true,
        numberOfMonths: 1,
        altField: "#alternate_start",
        altFormat: "yy-mm-dd",
        beforeShowDay: disableDates,
    }).on( "change", function() {
            to.datepicker( "option", "minDate", getDate( this ) );
        }),
    to = $( "#to" ).datepicker({
        defaultDate: "+1d",
        minDate: "+1d",
        maxDate: "+1y",
        changeMonth: true,
        numberOfMonths: 1,
        altField: "#alternate_end",
        altFormat: "yy-mm-dd",
        beforeShowDay: disableDates, 
    }).on( "change", function() {
            from.datepicker( "option", "maxDate", getDate( this ) );
        });

    function getDate( element ) {
        var date;
            try {
                date = $.datepicker.parseDate( dateFormat, element.value );
            } catch( error ) {
                date = null; 
            }
        return date;
    }
    function disableDates(date) {
        // Note : ClosedDates is initialized on window.load via an API ending point.
        // let ClosedDates = ["03-08-2021", "04-08-2021"];
        let noWeekend = jQuery.datepicker.noWeekends(date);
        let dt = $.datepicker.formatDate('dd-mm-yy', date);   
        // Jquery forum
        return noWeekend[0] ? (($.inArray(dt, ClosedDates) < 0) ? [true] : [false]) : noWeekend;
    }
    $.datepicker.setDefaults($.datepicker.regional['fr']) 
} );