define([
    'jquery', 
    'base/js/dialog', 
    'base/js/events',
    'notebook/js/codecell'
    ], function ($, dialog, events, codecell) {
    var api = "/spark/api/v1";
    var CodeCell = codecell.CodeCell;

    var show_running_jobs = function() {
        var element = $('<div/>');

        $.getJSON(api + '/applications').done(function(data) {
            data.forEach(function(e, i) {
                var application_div = $('<div/>');
                application_div.append($('<h5/>').text(e.name + ': ' + e.id));
                var application_table = $('<table/>').addClass('table table-hover');

                var header_row = $('<tr/>');
                header_row.append($('<th/>').text('Job ID'));
                header_row.append($('<th/>').text('Job Name'));
                header_row.append($('<th/>').text('Progress'));
                application_table.append(header_row);

                $.getJSON(api + '/applications/' + e.id + '/jobs').done(function (jobs) {
                    jobs.forEach(function(e, i) {
                        var row = $('<tr/>');
                        row.append($('<td/>').text(e.jobId));
                        row.append($('<td/>').text(e.name));
                        
                        var status_class;
                        switch(e.status) {
                            case 'SUCCEEDED':
                                status_class = 'progress-bar-success';
                                break;
                            case 'RUNNING':
                                status_class = 'progress-bar-info';
                                break;
                            case 'FAILED':
                                status_class = 'progress-bar-danger';
                                break;
                            case 'UNKNOWN':
                                status_class = 'progress-bar-warning';
                                break;
                        }
                        
                        var progress_bar_div = create_progress_bar(status_class, e.numCompletedTasks, e.numTasks);
                        // progress defined in percent

/*                        var progress = e.numCompletedTasks / e.numTasks * 100;

                        var progress_bar_div = $('<div/>').addClass('progress').css({'min-width': '100px', 'margin-bottom': 0});
                        var progress_bar = $('<div/>')
                            .addClass('progress-bar ' + status_class)
                            .attr('role', 'progressbar')
                            .attr('aria-valuenow', progress)
                            .attr('aria-valuemin', 0)
                            .attr('aria-valuemax', 100)
                            .css('width', progress + '%')
                            .text(e.numCompletedTasks + ' out of ' + e.numTasks + ' tasks');
                        progress_bar_div.append(progress_bar);*/
                        row.append($('<td/>').append(progress_bar_div));

                        application_table.append(row);
                    });
                });
                application_div.append(application_table);
                element.append(application_div);
            });
        });

        var modal = dialog.modal({
            title: "Running Spark Jobs",
            body: element,
            buttons: {
                "Close": {}
            }
        });
        modal.addClass("modal_stretch");
    };

    var create_progress_bar = function(status_class, completed, total) {
        // progress defined in percent
        var progress = completed / total * 100;
        console.log("Progress is " + progress);

        var progress_bar_div = $('<div/>').addClass('progress').css({'min-width': '100px', 'margin-bottom': 0});
        var progress_bar = $('<div/>')
            .addClass('progress-bar ' + status_class)
            .attr('role', 'progressbar')
            .attr('aria-valuenow', progress)
            .attr('aria-valuemin', 0)
            .attr('aria-valuemax', 100)
            .css('width', progress + '%')
            .text(completed + ' out of ' + total + ' tasks');
        progress_bar_div.append(progress_bar);
        return progress_bar_div;
    }

    var spark_progress_bar = function(event, data) {
        var cell = data.cell;
        if (is_spark_cell(cell)) {
            add_progress_bar(cell);
        }
    }

    var add_progress_bar = function(cell) {
        var progress_bar_div = cell.element.find('.progress');
        if (progress_bar_div.length < 1) {
            var input_area = cell.element.find('.input_area');

            progress_bar_div = create_progress_bar('progress-bar-info', 5, 5);
            progress_bar_div.appendTo(input_area);
        }
    }

    var is_spark_cell = function(cell) {
        // TODO: Find a way to detect if cell is actually running Spark
        return (cell instanceof CodeCell)
    }

    var load_ipython_extension = function () {

        events.on('execute.CodeCell', spark_progress_bar);

        Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Alt-S', show_running_jobs);
        Jupyter.toolbar.add_buttons_group([{    
            'label':    'show running Spark jobs',
            'icon':     'fa-tasks',
            'callback': show_running_jobs,
            'id':       'show_running_jobs'
        }]);
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});