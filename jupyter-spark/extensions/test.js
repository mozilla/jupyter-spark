function get_base_path() {
    var loc = window.location;
    var proto = loc.protocol;
    var host = loc.hostname;
    var port = loc.port;

    var base = proto + "//" + host;
    if (parseInt(port) != 80) {
        base += ":" + port;
    }
    return base;
}

define(function () {
    var spark_redirect_uri = get_base_path() + "/spark";

    var spark_notebook = function () {
        window.open(spark_redirect_uri);
    };

    var test_button = function () {
        if (!Jupyter.toolbar) {
            $([Jupyter.events]).on("app_initialized.NotebookApp", test_button);
            return;
        }

        Jupyter.toolbar.add_buttons_group([
            {
                'label'   : 'test spark request',
                'icon'    : 'fa-info-circle',
                'callback': spark_notebook,
                'id'      : 'spark_notebook'
            }
        ]);
    };

    var load_ipython_extension = function () {
        test_button();
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
});
