define(['jquery', 'base/js/dialog'], function ($, dialog) {
    var api = "/spark/api/v1";

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
                            // TODO: find error case status
                        }
                        
                        // progress defined in percent
                        var progress = e.numCompletedTasks / e.numTasks * 100;

                        var progress_bar_div = $('<div/>').addClass('progress').css({'min-width': '100px', 'margin-bottom': 0});
                        var progress_bar = $('<div/>')
                            .addClass('progress-bar ' + status_class)
                            .attr('role', 'progressbar')
                            .attr('aria-valuenow', progress)
                            .attr('aria-valuemin', 0)
                            .attr('aria-valuemax', 100)
                            .css('width', progress + '%')
                            .text(e.numCompletedTasks + ' out of ' + e.numTasks + ' tasks');
                        progress_bar_div.append(progress_bar);
                        row.append($('<td/>').append(progress_bar_div));

                        application_table.append(row);
                    })
                })
                application_div.append(application_table);
                element.append(application_div);
            });
        })

        var modal = dialog.modal({
            title: "Running Spark Jobs",
            body: element,
            buttons: {
                "Close": {}
            }
        });
        modal.addClass("modal_stretch");
    };

    var load_ipython_extension = function () {
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