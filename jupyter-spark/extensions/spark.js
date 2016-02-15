define(function () {
    var show_running_jobs = function() {

        var element = 'fffffffff';
        
        var modal = Jupyter.dialog.modal({
            title: "Running Spark Jobs",
            body: element,
            buttons: {
                "Close": {}
            }
        });
        modal.addClass("modal_stretch");
    };

    var load_ipython_extension = function () {
        Jupyter.keyboard_manager.command_shortcuts.add_shortcut('Alt-S', show_stats);
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});