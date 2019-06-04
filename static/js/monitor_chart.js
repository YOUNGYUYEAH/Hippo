$(document).ready(function() {
    $("#time_dropdown_main .dropdown-menu").click("[data-stopPropagtion]", function (e) {
        e.stopPropagation();
    });

    var today = new Date();
    var oneday = 1000 * 60 * 60 * 24;

    $("#begin_day_btn").click( function() {
        $("#begin_day").focus()
    });
    $("#end_day_btn").click( function() {
        $("#end_day").focus()
    });

    function DatePicker(beginSelector,endSelector){
        $(beginSelector).datepicker({
            language:  "en-IE",
            autoclose: true,
            format: "yyyy-mm-dd",
            orientation: 'bottom',
            startDate: new Date (today - (oneday * 14)),
            endDate:new Date()
        }).on('changeDate', function(ev){
            if(ev.date){
                $(endSelector).datepicker('setStartDate', new Date(ev.date.valueOf()))
            }else{
                $(endSelector).datepicker('setStartDate', null);
            }
        });

        $(endSelector).datepicker(
        {
            language:  "en-IE",
            autoclose: true,
            format: "yyyy-mm-dd",
            orientation: 'bottom',
            endDate:new Date()
        }).on('changeDate', function(ev){
            if(ev.date){
                $(beginSelector).datepicker('setEndDate', new Date(ev.date.valueOf()))
            }else{
                $(beginSelector).datepicker('setEndDate', new Date());
            }
        })
    }
    DatePicker("#begin_day","#end_day");

    function TimeClickFunc(_SetTime) {
        var maxNumber = _SetTime.find('input').attr("max");
        var minNumber = _SetTime.find('input').attr("min");
        _SetTime.find('.btn:first-of-type').click(function () {
            _SetTime.find("input").focus();
            if (parseInt(_SetTime.find('input').val()) >= minNumber && parseInt(_SetTime.find('input').val()) < 9) {
                _SetTime.find('input').attr('value', "0" + (parseInt(_SetTime.find('input').val(), 10) + 1));
            } else if ( parseInt(_SetTime.find('input').val()) >= 9 && parseInt(_SetTime.find('input').val()) < maxNumber) {
                _SetTime.find('input').attr('value',parseInt(_SetTime.find('input').val(), 10) + 1);
            } else {
                _SetTime.find('input').attr('value',"0"+minNumber);
            }
        });
        _SetTime.find('.btn:last-of-type').click(function () {
            _SetTime.find("input").focus();
            if (parseInt(_SetTime.find('input').val()) > minNumber && parseInt(_SetTime.find('input').val()) <= 10) {
                _SetTime.find('input').attr('value',"0" + (parseInt(_SetTime.find('input').val(), 10) - 1));
            } else if (parseInt(_SetTime.find('input').val()) > 9 && parseInt(_SetTime.find('input').val()) <= maxNumber) {
                _SetTime.find('input').attr('value', parseInt(_SetTime.find('input').val(), 10) - 1);
            } else {
                _SetTime.find('input').attr('value',maxNumber);
            }
        });
    }
    TimeClickFunc($("#begin_hour"));
    TimeClickFunc($("#begin_minute"));
    TimeClickFunc($("#end_hour"));
    TimeClickFunc($("#end_minute"));
});

function getSecond() {
    var _ns = new Date().getSeconds();
    if ( _ns < 10 ) { _ns = "0" + _ns; }
    return _ns;
}
$("#time_reset").click(function () {
    var _nowtime = new Date();
    var _nowtimeF = new Date().Format("yyyy-MM-dd hh:mm:ss");        //index.js编写的方法
    var _hourago = new Date(_nowtime - (1000 * 60 * 60)).Format("yyyy-MM-dd hh:mm:ss");
    var new_timerange = _hourago + " - " + _nowtimeF;
    $("#select_time").attr("value",new_timerange);
});

$("#begin_minute input").focus(function(){
    var _btm = $("#begin_minute input").val();
    var new_timerange = $("#begin_day").val() + " " + $("#begin_hour input").val() + ":" + _btm + ":" + getSecond()
        + " - " + $("#end_day").val() + " " + $("#end_hour input").val() + ":" + $("#end_minute input").val() + ":" + getSecond();
    $("#select_time").attr("value",new_timerange)
});
$("#begin_hour input").focus(function(){
    var _bth = $("#begin_hour input").val();
    var new_timerange = $("#begin_day").val() + " " + _bth + ":" + $("#begin_minute input").val() + ":" + getSecond()
        + " - " + $("#end_day").val() + " " + $("#end_hour input").val() + ":" + $("#end_minute input").val() + ":" + getSecond();
    $("#select_time").attr("value",new_timerange)
});
$("#end_minute input").focus(function(){
    var _etm = $("#end_minute input").val();
    var new_timerange = $("#begin_day").val() + " " + $("#begin_hour input").val() + ":" + $("#begin_minute input").val() + ":" + getSecond()
        + " - " + $("#end_day").val() + " " + $("#end_hour input").val() + ":" + _etm + ":" + getSecond();
    $("#select_time").attr("value",new_timerange)
});
$("#end_hour input").focus(function(){
    var _eth = $("#end_hour input").val();
    var new_timerange = $("#begin_day").val() + " " + $("#begin_hour input").val() + ":" + $("#begin_minute input").val() + ":" + getSecond()
        + " - " + $("#end_day").val() + " " + _eth + ":" + $("#end_minute input").val() + ":" + getSecond();
    $("#select_time").attr("value",new_timerange)
});

function PostTimeFunc(_timekey) {
    $("#time_dropdown_main .dropdown-menu").removeClass("show");
    var create_chart_ip = $("#select_ip").find("option:selected");
    var _chart_host_ip = create_chart_ip.text();
    if ( ! _timekey ) {
        var time_range = $("#select_time").val();
    } else {
        var _time_ago = new Date(new Date() - (1000 * 60 * 60 * _timekey)).Format("yyyy-MM-dd hh:mm:ss");
        var _time_now = new Date().Format("yyyy-MM-dd hh:mm:ss");
        var time_range = _time_ago + " - " + _time_now;
    }
    if ( ! create_chart_ip.prop("disabled") && create_chart_ip.val() !== "" ) {
        var _chart_ip = _chart_host_ip.split("(")[1].split(")")[0];
        var _chart_type = $("#select_type").find("option:selected").val();
        $.ajax({
            url: '/monitor/c',
            type: 'POST',
            cache: false,
            data: {'ip': _chart_ip,
                'type':_chart_type,
                'time_range': time_range
            },
            success: function(data, statsText, xhr) {
                if ( xhr.status === 200) {
                    CreateChartFunc(_chart_host_ip,_chart_type,data);
                    $("body").addClass("sidenav-toggled");
                    $(".navbar-sidenav .nav-link-collapse").addClass("collapsed");
                    $(".navbar-sidenav .sidenav-second-level, .navbar-sidenav .sidenav-third-level").removeClass("show");
                    $("#Chartsweb").removeAttr("hidden");
                }
            },
        })
    } else {
        alert("Please Select IP For Create Charts.");
    }
}
function ChangeDayFunc (k) {
    $("#"+k+"_day").attr("value",$("#"+k+"_day").val());
    var _new_timerange = $("#begin_day").val() + " " + $("#begin_hour input").val() + ":" + $("#begin_minute input").val() + ":" + getSecond()
        + " - " + $("#end_day").val() + " " + $("#end_hour input").val() + ":" + $("#end_minute input").val() + ":" + getSecond();
    $("#select_time").attr("value",_new_timerange);
}
