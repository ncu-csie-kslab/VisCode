define(["require", "jquery", "base/js/namespace", "base/js/events", "base/js/utils", "base/js/dialog"], function (require, $, IPython, events, utils, dialog) {

    function addAnnouncement(title, content) {
        $('#tab_content').prepend('<div class="panel panel-default" style=""><div class="panel-heading">' + title + '</div><div class="panel-body">' + content + '</div></div>')
    }

    function load() {
        var settings = {
            url: utils.get_body_data("baseUrl") + 'viscode/announcement',
            processData: false,
            type: "GET",
            dataType: "json",
            contentType: 'application/json',
            success: function (data) {
                for (var i = 0; i < data.normalAnnouncements.length; i++) {
                    var announcement = data.normalAnnouncements[i]
                    if(announcement.shown){
                        addAnnouncement(announcement.title, announcement.content)
                    }
                }
                for (var i = 0; i < data.systemAnnouncements.length; i++) {
                    var announcement = data.systemAnnouncements[i]
                    if(announcement.shown){
                        addAnnouncement(announcement.title, announcement.content)
                    }
                }
            }
        };
        utils.ajax(settings);
    }

    return {
        load_ipython_extension: load
    };

});