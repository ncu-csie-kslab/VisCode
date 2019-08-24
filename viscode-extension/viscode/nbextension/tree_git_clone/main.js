define(["require", "jquery", "base/js/namespace", "base/js/events", "base/js/utils"], function (require, $, IPython, events, utils) {

    function load() {
        $('#notebook_toolbar > .tree-buttons > .pull-right').prepend('<button class="btn btn-default btn-xs">Clone</button>')
    }

    return {
        load_ipython_extension: load
    };

});