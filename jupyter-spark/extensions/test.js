define(function () {
    var spark_notebook = function () {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/spark/api/v1/applications", true);
        xhr.onload = function() {
            window.alert(this.responseText);
        }
        xhr.send();
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
