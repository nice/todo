$(document).ready(function() {
    // common vars
    $task_modal = $('#taskModal');
    $task_form = $('#task-form');
    $task_submit = $('#task-submit');
    $task_inputs = $('#task-inputs');
    $ajax_loader = $('.ajax-loader');

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

    // ajax loading display
    function ajaxify(ele) {
        $(ele).after($ajax_loader);
        $ajax_loader.show();
    }

    function dejaxify() {
        $ajax_loader.remove();
    }

    function task_form_validate() {
        var error = false;
        $name = $('#id_name');
        $description = $('#id_description');
        $due_date = $('#id_due_date');
        function danger(ele) {
            error = true;
            $(ele).addClass('danger');
        }
        function clean(ele) {
            $(ele).removeClass('danger');
        }
        clean($name); clean($description); clean($due_date);
        if ($name.val() == '') {
            danger($name)
        }
        if ($description.val() == '') {
            danger($description);
        }
        if($due_date.val() == '') {
            danger($description);
        }
        return error;
    }

    // datepicker settings
    $('.date').datepicker({
        format: "yyyy-mm-dd",
    });

    // new task action
    $('.new-task').click(function() {
        $task_modal.find('.modal-title').text('Add new task.');
        $task_form.attr('action', '/task/');
        $task_inputs.show();
        $task_inputs.find('#id_name').val('');
        $task_inputs.find('#id_description').val('');
        $task_inputs.find('#id_due_date').val('');
        $task_submit.attr('value', 'Create');
    });

    $task_form.submit(function(e) {
        var error = task_form_validate();
        if (!error) {
            $(this).submit();
        }
        e.preventDefault();
    });

    // edit task action
    $('.edit-task').click(function() {
        ajaxify($task_inputs);
        var id = $(this).closest('tr').data('id');
        $task_modal.find('.modal-title').text('Edit existing task.');
        $task_form.attr('action', '/task/{0}/'.format(id));
        $task_submit.attr('value', 'Update');
        $task_inputs.hide();
        $.getJSON('/view-task/?id={0}'.format(id), function(data) {
            var task = jQuery.parseJSON(data).fields;
            $task_inputs.find('#id_name').val(task.name);
            $task_inputs.find('#id_description').val(task.description);
            $task_inputs.find('#id_due_date').val(task.due_date);
            $task_inputs.show();
            dejaxify();
        });
    });

    //delete task action
    $('.delete-task').click(function() {
        var id = $(this).closest('tr').data('id');
        var sure = confirm('Are you sure you want to delete?');
        if (sure) {
            $.ajax({
                url: '/delete-task/',
                type: 'POST',
                data: {
                    id: id,
                },
                success: function(data) {
                    console.log('task deleted');
                }
            });
        }
    });

    // priority updation
    $('.task-priority').change(function() {
        ajaxify(this);
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
                dejaxify(this);
            }
        });
    });

    // state updation
    $('.task-state').change(function() {
        ajaxify(this);
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
                if ( $tr.hasClass('expired') && state != 'done') {
                    //do nothing 
                } else {
                    $tr.removeClass();
                    $tr.addClass(state);
                }
                console.log('state updated');
                dejaxify();
            }
        });
    });

    //view task
    $('.view-task').click(function() {
        ajaxify('.generic-body');
        var id = $(this).closest('tr').data('id');
        var $modal = $('#genericModal');
        $.ajax({
            url: '/view-task/',
            type: 'GET',
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
                $modal.find('.generic-body').html(html);
                dejaxify();
            }
        });
    });
});
