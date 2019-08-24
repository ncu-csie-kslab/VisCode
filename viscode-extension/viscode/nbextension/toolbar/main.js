define(["require", "jquery", "base/js/namespace", "base/js/events", "base/js/utils", "base/js/dialog", 'base/js/i18n'], function (require, $, IPython, events, utils, dialog, i18n) {

    function largeModal(options) {

        var modal = $("<div/>")
            .addClass("modal")
            .addClass("fade")
            .attr("role", "dialog");
        var dialog = $("<div/>")
            .addClass("modal-dialog")
            .addClass("modal-lg")
            .appendTo(modal);
        var dialog_content = $("<div/>")
            .addClass("modal-content")
            .appendTo(dialog);
        if (typeof (options.body) === 'string' && options.sanitize !== false) {
            options.body = $("<p/>").text(options.body);
        }
        dialog_content.append(
            $("<div/>")
            .addClass("modal-header")
            .mousedown(function () {
                $(".modal").draggable({
                    handle: '.modal-header'
                });
            })
            .append($("<button>")
                .attr("type", "button")
                .addClass("close")
                .attr("data-dismiss", "modal")
                .attr("aria-hidden", "true")
                .html("&times;")
            ).append(
                $("<h4/>")
                .addClass('modal-title')
                .text(options.title || "")
            )
        ).append(
            $("<div/>")
            .addClass("modal-body")
            .append(
                options.body || $("<p/>")
            )
        );

        var footer = $("<div/>").addClass("modal-footer");

        var default_button;

        for (var label in options.buttons) {
            var btn_opts = options.buttons[label];
            var button = $("<button/>")
                .addClass("btn btn-default btn-sm")
                .attr("data-dismiss", "modal")
                .text(i18n.msg.translate(label).fetch());
            if (btn_opts.id) {
                button.attr('id', btn_opts.id);
            }
            if (btn_opts.click) {
                button.click($.proxy(btn_opts.click, dialog_content));
            }
            if (btn_opts.class) {
                button.addClass(btn_opts.class);
            }
            footer.append(button);
            if (options.default_button && label === options.default_button) {
                default_button = button;
            }
        }
        if (!options.default_button) {
            default_button = footer.find("button").last();
        }
        dialog_content.append(footer);
        // hook up on-open event
        modal.on("shown.bs.modal", function () {
            setTimeout(function () {
                default_button.focus();
                if (options.open) {
                    $.proxy(options.open, modal)();
                }
            }, 0);
        });

        // destroy modal on hide, unless explicitly asked not to
        if (options.destroy === undefined || options.destroy) {
            modal.on("hidden.bs.modal", function () {
                modal.remove();
            });
        }
        modal.on("hidden.bs.modal", function () {
            if (options.notebook) {
                var cell = options.notebook.get_selected_cell();
                if (cell) cell.select();
            }
            if (options.keyboard_manager) {
                options.keyboard_manager.enable();
                options.keyboard_manager.command_mode();
            }
        });

        if (options.keyboard_manager) {
            options.keyboard_manager.disable();
        }

        if (options.backdrop === undefined) {
            options.backdrop = 'static';
        }

        return modal.modal(options);
    };

    function getAnnouncement(callback) {
        var settings = {
            url: utils.get_body_data("baseUrl") + 'viscode/announcement',
            processData: false,
            type: "GET",
            dataType: "json",
            contentType: 'application/json',
            success: function (data) {
                callback(data);
            }
        };
        utils.ajax(settings);
    };

    function showSystemAnnouncementSettingModal() {
        dialog.modal({
            title: '系統公告設定',
            sanitize: false,
            body: '',
            buttons: {
                OK: {
                    class: 'btn-success'
                }
            }
        });
    }

    function showNormalAnnouncementSettingModal() {
        var form = $('<form>');
        var input = $('<div class="form-group"><label for="announcement-text">Content:</label><textarea id="announcement-text" class="form-control" rows="10" hidden required></textarea></div>');
        form.append(input); 
        var ed;
        $.getScript('https://cdnjs.cloudflare.com/ajax/libs/tinymce/5.0.3/tinymce.min.js', function () {
            getAnnouncement(function (data) {
                var normalAnnouncement = data.normalAnnouncements[0];
                form.find('#announcement-text').val(normalAnnouncement.content);
                largeModal({
                    title: '一般公告設定',
                    sanitize: false,
                    body: form,
                    open: function () {
                        ed = tinymce.createEditor('announcement-text', {
                            height: '50vh',
                            min_height: 400,
                            plugins: 'code link autolink emoticons',
                            menubar: "insert",
                            toolbar: "undo redo bold italic alignleft aligncenter alignright bullist numlist outdent indent code forecolor backcolor link emoticons"
                        });
                        ed.render();
                    },
                    buttons: {
                        OK: {
                            class: 'btn-success',
                            click: function (event) {
                                var dialogContent = $(this);
                                var form = dialogContent.find('form');
                                var text = ed.getContent();
                                var data = {
                                    type: 'normal',
                                    text: text
                                }
                                var settings = {
                                    url: utils.get_body_data("baseUrl") + 'viscode/announcement',
                                    processData: false,
                                    type: "POST",
                                    data: JSON.stringify(data),
                                    dataType: "json",
                                    contentType: 'application/json',
                                    success: function (data) {
                                        if (data.isError) {
                                            alert('修改失敗！\n' + data.msg);
                                            return;
                                        }
                                        alert('修改成功！');
                                    },
                                    error: function () {
                                        alert('修改失敗！');
                                    }

                                };
                                utils.ajax(settings);
                            }
                        },
                        Cancel: {
                            class: 'btn-default'
                        }
                    }
                });

            });
        });
    };

    function showAddAccountModal() {
        var form = $('<form autocomplete="off" />');
        var accountInput = $('<div class="form-group"><label for="new-account-input">帳號:</label><input id="new-account-input" class="form-control" type="text" autocomplete="off" required/></div>');
        var passwordInput = $('<div class="form-group"><label for="new-password-input">密碼:</label><input id="new-password-input" class="form-control" type="password" autocomplete="off" required/></div>');
        var error = $('<div/>').css('color', 'red');
        form.append(accountInput, passwordInput, error);
        dialog.modal({
            title: '新增帳號',
            sanitize: false,
            body: form,
            buttons: {
                Add: {
                    class: 'btn-primary',
                    click: function (event) {
                        var dialogContent = $(this);
                        var form = dialogContent.find('form');
                        var account = form.find('#new-account-input').val();
                        var password = form.find('#new-password-input').val();
                        var data = {
                            account: account,
                            password: password
                        }
                        var settings = {
                            url: utils.get_body_data("baseUrl") + 'viscode/users',
                            processData: false,
                            type: "POST",
                            data: JSON.stringify(data),
                            dataType: "json",
                            contentType: 'application/json',
                            success: function (data) {
                                if (data.isError) {
                                    alert('新增失敗！\n' + data.msg);
                                    return;
                                }
                                alert('新增成功！');
                            },
                            error: function (data) {
                                if (data.isError && data.msg)
                                alert('新增失敗！');
                            }
                        };
                        if (account.length == 0) {
                            error.text('帳號不能為空白');
                            return false;
                        }
                        if (password.length < 4) {
                            error.text('密碼至少需要4個字元');
                            return false;
                        }

                        utils.ajax(settings);
                    }
                },
                Close: {
                    class: 'btn-default'
                }
            }
        });
    }

    function showUpdateAccountModal() {
        var form = $('<form autocomplete="off" />');
        var accountInput = $('<div class="form-group"><label for="account-input">帳號:</label><input id="account-input" class="form-control" type="text" autocomplete="off" required/></div>');
        var passwordInput = $('<div class="form-group"><label for="new-password-input">密碼:</label><input id="new-password-input" class="form-control" type="password" autocomplete="off" required/></div>');
        var error = $('<div/>').css('color', 'red');
        form.append(accountInput, passwordInput, error);
        dialog.modal({
            title: '修改帳號',
            sanitize: false,
            body: form,
            buttons: {
                Add: {
                    class: 'btn-primary',
                    click: function (event) {
                        var dialogContent = $(this);
                        var form = dialogContent.find('form');
                        var account = form.find('#account-input').val();
                        var password = form.find('#new-password-input').val();
                        var data = {
                            account: account,
                            password: password
                        }
                        var settings = {
                            url: utils.get_body_data("baseUrl") + 'viscode/users',
                            processData: false,
                            type: "PATCH",
                            data: JSON.stringify(data),
                            dataType: "json",
                            contentType: 'application/json',
                            success: function (data) {
                                if (data.isError) {
                                    alert('修改失敗！\n' + data.msg);
                                    return;
                                }
                                alert('修改成功！');
                            },
                            error: function (data) {
                                if (data.isError && data.msg)
                                alert('修改失敗！');
                            }
                        };
                        if (account.length == 0) {
                            error.text('帳號不能為空白');
                            return false;
                        }
                        if (password.length < 4) {
                            error.text('密碼至少需要4個字元');
                            return false;
                        }

                        utils.ajax(settings);
                    }
                },
                Close: {
                    class: 'btn-default'
                }
            }
        });
    }

    function showAdminModal() {
        var systemAnnouncementBtn = $('<div class="col-sm-3"><button class="btn btn-default">設定系統公告</button></div>').click(showSystemAnnouncementSettingModal);
        var normalAnnouncementBtn = $('<div class="col-sm-3"><button class="btn btn-default">設定一般公告</button></div>').click(showNormalAnnouncementSettingModal);
        var dialogAnnouncementBtn = $('<div class="col-sm-3"><button class="btn btn-default">設定彈出公告</button></div>');
        var addAccountBtn = $('<div class="col-sm-3"><button class="btn btn-default">新增帳號</button></div>').click(showAddAccountModal);
        var changeAccountPasswordBtn = $('<div class="col-sm-3"><button class="btn btn-default">修改帳號密碼</button></div>').click(showUpdateAccountModal);
        var row = $('<div class="row admin-modal" style="text-align: center;"></div>').append(systemAnnouncementBtn, normalAnnouncementBtn, dialogAnnouncementBtn, addAccountBtn, changeAccountPasswordBtn);
        var body = $('<div class="container-fliud"></div>').append(row);
        dialog.modal({
            title: 'Admin',
            sanitize: false,
            body: body,
            buttons: {
                Close: {
                    class: 'btn-default'
                }
            }
        });
    }

    function showDashboardModal() {
        var errorPiePlot = $('<div class="col-md-6"><iframe src="https://viscode-kibana.moocs.tw/app/kibana#/visualize/edit/391e8e30-3dcb-11e9-89b1-6fd57c7b5d6d?embed=true&_g=(refreshInterval:(pause:!t,value:0),time:(from:now-15m,mode:quick,to:now))&_a=(filters:!(),linked:!f,query:(language:lucene,query:\'\'),uiState:(),vis:(aggs:!((enabled:!t,id:\'1\',params:(),schema:metric,type:count),(enabled:!t,id:\'2\',params:(field:errorName.keyword,missingBucket:!f,missingBucketLabel:Missing,order:desc,orderBy:\'1\',otherBucket:!f,otherBucketLabel:Other,size:10),schema:segment,type:terms)),params:(addLegend:!t,addTooltip:!t,isDonut:!t,labels:(last_level:!t,show:!f,truncate:100,values:!t),legendPosition:right,type:pie),title:\'error+percentage\',type:pie))" height="500px" width="100%"></iframe></div>');
        var userErrorTypeChart = $('<div class="col-md-6"><iframe src="https://viscode-kibana.moocs.tw/app/kibana#/visualize/edit/beb9f790-3e5d-11e9-89b1-6fd57c7b5d6d?embed=true&_g=(refreshInterval:(pause:!f,value:10000),time:(from:now-15m,mode:quick,to:now))&_a=(filters:!(),linked:!f,query:(language:lucene,query:\'\'),uiState:(),vis:(aggs:!((enabled:!t,id:\'1\',params:(),schema:metric,type:count),(enabled:!t,id:\'2\',params:(field:username.keyword,missingBucket:!f,missingBucketLabel:Missing,order:desc,orderBy:\'1\',otherBucket:!f,otherBucketLabel:Other,size:50),schema:segment,type:terms),(enabled:!t,id:\'3\',params:(field:errorName.keyword,missingBucket:!f,missingBucketLabel:Missing,order:desc,orderBy:\'1\',otherBucket:!f,otherBucketLabel:Other,size:10),schema:group,type:terms)),params:(addLegend:!t,addTimeMarker:!f,addTooltip:!t,categoryAxes:!((id:CategoryAxis-1,labels:(show:!t,truncate:100),position:bottom,scale:(type:linear),show:!t,style:(),title:(),type:category)),grid:(categoryLines:!f,style:(color:%23eee)),legendPosition:right,seriesParams:!((data:(id:\'1\',label:Count),drawLinesBetweenPoints:!t,mode:stacked,show:true,showCircles:!t,type:histogram,valueAxis:ValueAxis-1)),times:!(),type:histogram,valueAxes:!((id:ValueAxis-1,labels:(filter:!f,rotate:0,show:!t,truncate:100),name:LeftAxis-1,position:left,scale:(mode:normal,type:linear),show:!t,style:(),title:(text:Count),type:value))),title:\'users+error+type\',type:histogram))" height="500" width="100%"></iframe></div>');
        var dashboard = $('<div class="col-md-12"></div>')
        // var dashboard = $('<div class="col-md-12"></div>').load(require.toUrl('./index.html'))
        var dashboardIframe = $('<iframe></iframe>').attr({
            src: require.toUrl('./index.html'),
            width: '100%',
            height: '600px'
        })
        dashboard.append(dashboardIframe)
        var body = $('<div class="row"></div>').append(userErrorTypeChart, errorPiePlot, dashboard)


        largeModal({
            title: 'Dashboard',
            sanitize: false,
            body: body,
            buttons: {
                OK: {
                    class: 'btn-success'
                }
            }
        });
    }

    function addAdminButton() {
        $('#viscode-toolbar')
            .append('<div id="viscode-toolbar-admin-btn" class="viscode-toolbar-btn"><header>Admin</header></div>');
        $('#viscode-toolbar-admin-btn').click(showAdminModal);
    };

    function addDashboardButton() {
        $('#viscode-toolbar').append('<div id="viscode-toolbar-dashboard-btn" class="viscode-toolbar-btn"><header>Dashboard</header></div>');
        $('#viscode-toolbar-dashboard-btn').click(showDashboardModal);
    };

    function showToolbar(role) {

        $('<link>')
            .appendTo('head')
            .attr({
                type: 'text/css',
                rel: 'stylesheet',
                href: require.toUrl('./style.css')
            });
        $('<script>')
            .appendTo('head')
            .attr({
                src: 'https://cdnjs.cloudflare.com/ajax/libs/d3/4.13.0/d3.js'
            });
        $('<script>')
            .appendTo('head')
            .attr({
                src: require.toUrl('./radarChart.js')
            });

        $('body').append('<div id="viscode-toolbar" class="" style="position:fixed; bottom: 0px; right: 0px;"></div>');

        addDashboardButton()

        if (role == 'admin') {
            addAdminButton();
        }

    };

    function load() {

        var settings = {
            url: utils.get_body_data("baseUrl") + 'viscode/role',
            processData: false,
            type: "GET",
            dataType: "json",
            contentType: 'application/json',
            success: function (data) {
                if (data.role == 'admin') {
                    showToolbar(data.role);
                }
            }
        };
        utils.ajax(settings);

    }

    return {
        load_ipython_extension: load
    };

});