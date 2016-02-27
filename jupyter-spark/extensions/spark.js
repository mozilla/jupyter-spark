var api = "/spark/api/v1";
var update_frequency = 10000; // ms


/* 
cache is an array of application objects with an added property jobs.
application.jobs is the result of the /applications/applicationId/jobs
API request.
*/
var cache = [];

var update = function() {
    update_cache(update_dialog_contents);
};

// callbacks follows jQuery callback style, can be either single function or array of functions
// callbacks will be passed the cache as a parameter
var update_cache = function(callbacks) {
    var cbs;
    if (callbacks) {
        cbs = $.Callbacks();
        cbs.add(callbacks);
    }
    $.getJSON(api + '/applications').done(function(applications) {
        applications.forEach(function(application, i) {
            $.getJSON(api + '/applications/' + application.id + '/jobs').done(function (jobs) {
                cache[i] = application;
                cache[i].jobs = jobs;
                if (cbs) {
                    // FIXME: need to check if all applications have been updated
                    cbs.fire(cache);
                }
            });
        });
    });
};

var update_dialog_contents = function() {
    if ($('#dialog_contents').length) {
        var element = $('<div/>').attr('id', 'dialog_contents');
        cache.forEach(function(application, i){
            element.append(create_application_table(application));
        });

        $('#dialog_contents').replaceWith(element);
    }
};

var create_application_table = function(e) {
    var application_div = $('<div/>');
    application_div.append($('<h5/>').text(e.name + ': ' + e.id));
    var application_table = $('<table/>').addClass('table table-hover');

    var header_row = $('<tr/>');
    header_row.append($('<th/>').text('Job ID'));
    header_row.append($('<th/>').text('Job Name'));
    header_row.append($('<th/>').text('Progress'));
    application_table.append(header_row);

    e.jobs.forEach(function(job, i) {
        application_table.append(create_table_row(job));
    });

    application_div.append(application_table);
    return application_div;
};

var create_table_row = function(e) {
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
    
    // progress defined in percent
    var progress = e.numCompletedTasks / e.numTasks * 100;

    var progress_bar_div = $('<div/>').addClass('progress').css({'min-width': '100px', 'margin-bottom': 0});
    var progress_bar = $('<div/>')
        .addClass('progress-bar ' + status_class)
        .attr('role', 'progressbar')
        .attr('aria-valuenow', progress)
        .attr('aria-valuemin', 0)
        .attr('aria-valuemax', 100)
        .css({'width': progress + '%', 'min-width': '10px'})
        .text(e.numCompletedTasks + ' out of ' + e.numTasks + ' tasks');
    progress_bar_div.append(progress_bar);
    row.append($('<td/>').append(progress_bar_div));
    return row;
};


define(['jquery', 'base/js/dialog'], function ($, dialog) {

    var show_running_jobs = function() {
        var element = $('<div/>').attr('id', 'dialog_contents');
        var modal = dialog.modal({
            title: "Running Spark Jobs",
            body: element,
            buttons: {
                "Close": {}
            },
            open: update_dialog_contents
        });
    };

    var load_ipython_extension = function () {
        Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Alt-S', show_running_jobs);
        Jupyter.toolbar.add_buttons_group([{    
            'label':    'show running Spark jobs',
            'icon':     'fa-tasks',
            'callback': show_running_jobs,
            'id':       'show_running_jobs'
        }]);
        update();
        window.setInterval(update, update_frequency);
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});