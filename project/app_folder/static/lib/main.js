$(document).ready(function() {

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        
        defaultDate: '2020-05-03',
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: {
            url: 'data',
            error: function() {
                $('#script-warning').show();
            }
        },
        loading: function(bool) {
            $('#loading').toggle(bool);
        },
            
            });
        });
