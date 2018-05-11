import "./spark.css";

import "bootstrap/dist/css/bootstrap.min.css";

import {
    JupyterLab, JupyterLabPlugin
} from '@jupyterlab/application';

import {
    NotebookActions, NotebookPanel, INotebookModel
} from '@jupyterlab/notebook';

import {
    ToolbarButton
} from '@jupyterlab/apputils';

import {
    IDisposable, DisposableDelegate
} from '@phosphor/disposable';

import {
    Widget, PanelLayout
} from '@phosphor/widgets';

var common = require('./extension.js');

const plugin = {
    id: 'jupyter_spark',
    autoStart: true,
    activate: (app) => {
        let api_url = "/spark/api/v1";
        let widget = new Widget();
        widget.id = 'jupyter-spark';
        widget.class = 'jupter-spark-panel';
        widget.title.label = 'Spark';
        widget.title.closable = true;

        widget.onBeforeShow = (msg) => {
            widget.intervalId = window.setInterval(common().update, 500, api_url);
        };

        widget.onBeforeHide = (msg) => {
            window.clearInterval(widget.intervalId);
        };

        let div = document.createElement('div');
        div.id = "spark_dialog_contents";
        widget.node.appendChild(div);

        app.shell.addToLeftArea(widget);
    }
};

export default plugin;
