$(document).ready(function() {
    // string format
    if (!String.prototype.format) {
      String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) { 
          return typeof args[number] != 'undefined'
            ? args[number]
            : match
          ;
        });
      };
    }

    // sort table
    function sortTable(table, order) {
        var asc   = order === 'asc',
            tbody = table.find('tbody');

        tbody.find('tr').sort(function(a, b) {
            if (asc) {
                return $('td:first select', a).val().localeCompare($('td:first select', b).val());
            } else {
                return $('td:first select', b).val().localeCompare($('td:first select', a).val());
            }
        }).appendTo(tbody);
    }

    // datepicker settings
    $('.date').datepicker({
        format: "yyyy-mm-dd",
    });

    // taskform validation

    // priority updation
    $('.task-priority').change(function() {
        var id = $(this).closest('tr').data('id');
        var priority = $(this).val();
        $.ajax({
            url: '/update-task/priority/',
            type: 'POST',
            data: {
                id: id,
                priority: priority
            },
            success: function(data) {
                sortTable($('#tasks'),'asc');
                console.log('priority updated');
            }
        });
    });

    // state updation
    $('.task-state').change(function() {
        var $tr = $(this).closest('tr');
        var id = $tr.data('id');
        var state = $(this).val();
        $.ajax({
            url: '/update-task/state/',
            type: 'POST',
            data: {
                id: id,
                state: state 
            },
            success: function(data) {
                $tr.removeClass();
                $tr.addClass(state);
                console.log('state updated');
            }
        });
    });

    //view task
    $('.view-task').click(function() {
        var id = $(this).closest('tr').data('id');
        var $modal = $('#genericModal');
        $.ajax({
            url: '/view-task/',
            type: 'POST',
            data: {
                id: id,
            },
            dataType: 'json',
            success: function(data) {
                var task = jQuery.parseJSON(data).fields;
                var html = "<p><u><b>{0}</b></u></>".format(task.name);
                html += "<p>{0}</p>".format(task.description);
                html += "<p><b>Priority:</b> {0} / <b>Due Date: </b>{1} / <span class='{2}'<b>State:</b> {2}</span></p>".format(
                    task.priority, task.due_date, task.state
                );
                $modal.find('.modal-body').html(html);
            }
        });
    });


    // edit task
    $('.view-task').click(function() {
        var id = $(this).closest('tr').data('id');
    });

});
