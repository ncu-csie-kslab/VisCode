define(["require", "jquery", "base/js/namespace", "base/js/events", "base/js/utils"], function (require, $, IPython, events, utils) {
    "use strict";

    var data = {
        notebookPath: utils.get_body_data("notebookPath")
    }

    var settings = {
        url: utils.get_body_data("baseUrl") + 'viscode/tree_logs',
        processData: false,
        type: "POST",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: 'application/json'
    };
    utils.ajax(settings);

});