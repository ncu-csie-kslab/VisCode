define(["require", "jquery", "base/js/namespace", "base/js/events", "base/js/utils"], function (require, $, IPython, events, utils) {
    "use strict";

    var firstExecTime = null;
    var execCells = [];
    var toggle_all = null;

    // var month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    // var day_names = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

    var timestamp = null;

    var patchCodecellExecute = function () {
        console.log('patching codecell to trigger ExecuteCell.ExecuteTime');
        IPython.CodeCell.prototype.old_execute = IPython.CodeCell.prototype.execute;

        IPython.CodeCell.prototype.execute = function () {
            this.old_execute(arguments);
            events.trigger('ExecuteCell.ExecuteTime');
        };
    }

    // var date_fmt = function(date) {
    //     var dnames=day_names[date.getDay()] + "";
    //     var mon=month_names[date.getMonth()] + " ";
    //     var day=date.getDate() +" ";
    //     var year= date.getFullYear()+" ";

    //     var hour = date.getHours();
    //     var a_p = (hour < 12) ? "AM" : "PM";

    //     hour = (hour == 0) ? 12 : hour;
    //     hour = (hour > 12) ? hour - 12 : hour;

    //     var min = date.getMinutes() + "";
    //     min = (min.length == 1) ? "0" + min: min;

    //     var sec = date.getSeconds() + "";
    //     sec = (sec.length == 1) ? "0" + sec: sec;

    //     return dnames+ ', ' + mon + day + year + 'at ' + hour + ":" + min + ":" + sec + " " + a_p;
    // }

    var executionStartTime = function (event) {
        var cell = IPython.notebook.get_selected_cell(); // get the selected cell
        if (cell instanceof IPython.CodeCell) {
            var ce = cell.element;

            var execTime = new Date();
            timestamp = execTime.getTime();

            if (firstExecTime === null)
                firstExecTime = execTime;
            execCells.push([IPython.notebook.get_selected_index()]);

            // console.log('Start time: ' + date_fmt(execTime));
            // console.log('Notebook name: ' + IPython.notebook.get_notebook_name());
            // console.log(ce[0].innerText);
            // console.log(cell);

            // var output_str = "exec_ts: " + timestamp + "\n" +
            //                  "start_time: " + date_fmt(execTime) + "\n" +
            //                 "notebook: " + IPython.notebook.get_notebook_name() + "\n" +
            //                 "text: " + ce[0].innerText;

            //var output_str;
            //if( typeof(cell.output_area.outputs[0]) !== 'undefined'){
            //    output_str = cell.output_area.outputs[0].output_type == "error" ? "Error" : "Pass";
            //} else {
            //    output_str = "Pass";
            //}

            //var settings = {
            //  url: utils.get_body_data("baseUrl")+'scipy/log',
            //  processData: false,
            //  type: "PUT",
            //  data: output_str,
            //  dataType: "json",
            //  contentType: 'application/json'
            //};
            //utils.ajax(settings);
        }
    };

    var executionEndTime = function (event) {

        if (firstExecTime === null) {
            return;
        }

        var cellNb = execCells.shift();

        var cell = IPython.notebook.get_cell(cellNb); // get the selected cell
        if (cell instanceof IPython.CodeCell) {

            // var endExecTime=new Date();

            // var UnixBeforeExec = firstExecTime.getTime()/1000;
            // var end = endExecTime.getTime()/1000;
            // var ET = Math.round((end-UnixBeforeExec)*1000)/1000;

            // if (!execCells.length) {
            //     firstExecTime=null;
            // } else {
            //     firstExecTime=endExecTime;
            // }

            // console.log("Elapsed Time: " + ET);

            // var output_str = "exec_ts: " + timestamp + "\n" +
            //                 "end_time: " + date_fmt(endExecTime) + "\n" +
            //                 "notebook: " + IPython.notebook.get_notebook_name() + "\n" +
            //                 "output: " + cell.output_area.element[0].innerText;

            var output;
            if (typeof (cell.output_area.outputs[0]) !== 'undefined' && cell.output_area.outputs[0].output_type == "error") {
                output = {
                    isError: true,
                    errorName: cell.output_area.outputs[0].ename
                };
            } else {
                output = {
                    isError: false
                };
            }


            var settings = {
                url: utils.get_body_data("baseUrl") + 'scipy/log',
                processData: false,
                type: "POST",
                data: JSON.stringify(output),
                dataType: "json",
                contentType: 'application/json'
            };
            utils.ajax(settings);

        }
    };

    var load_ipython_extension = function () {
        patchCodecellExecute();

        events.on('ExecuteCell.ExecuteTime', executionStartTime);
        events.on('kernel_idle.Kernel', executionEndTime);
    };

    var extension = {
        load_ipython_extension: load_ipython_extension
    };
    return extension;
});