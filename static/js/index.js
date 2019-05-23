(function($) {
    "use strict"; // Start of use strict
    // Configure tooltips for collapsed side navigation
    $('.navbar-sidenav [data-toggle="tooltip"]').tooltip({
        template: '<div class="tooltip navbar-sidenav-tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
    });
    // Toggle the side navigation
    $("#sidenavToggler").click(function(e) {
        e.preventDefault();
        $("body").toggleClass("sidenav-toggled");
        $(".navbar-sidenav .nav-link-collapse").addClass("collapsed");
        $(".navbar-sidenav .sidenav-second-level, .navbar-sidenav .sidenav-third-level").removeClass("show");
    });
    // Force the toggled class to be removed when a collapsible nav link is clicked
    $(".navbar-sidenav .nav-link-collapse").click(function(e) {
        e.preventDefault();
        $("body").removeClass("sidenav-toggled");
    });
    // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
    $('body.fixed-nav .navbar-sidenav, body.fixed-nav .sidenav-toggler, body.fixed-nav .navbar-collapse').on('mousewheel DOMMouseScroll', function(e) {
        var e0 = e.originalEvent,
            delta = e0.wheelDelta || -e0.detail;
        this.scrollTop += (delta < 0 ? 1 : -1) * 30;
        e.preventDefault();
    });
    // Scroll to top button appear
    $(document).scroll(function() {
        var scrollDistance = $(this).scrollTop();
        if (scrollDistance > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });
    // Configure tooltips globally
    $('[data-toggle="tooltip"]').tooltip()
    // Smooth scrolling using jQuery easing
    $(document).on('click', 'a.scroll-to-top', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top)
        }, 1000, 'easeInOutExpo');
            event.preventDefault();
    });
})(jQuery); // End of use strict


function monitordata(){
    /* 加载monitor_data页面 */
    var cssfilesText = "";
    cssfilesText += "<link href='/static/vendor/datatables/dataTables.bootstrap4.css' rel='stylesheet' type='text/css'>";
    cssfilesText += "<link href='/static/vendor/bootstrap-select-1.13.10/css/bootstrap-select.min.css' rel='stylesheet' type='text/css'>";
    cssfilesText += "<link href='/static/css/monitor.css' rel='stylesheet' type='text/css'>";
    var jsfilesText = "";
    jsfilesText += "<script src='/static/vendor/datatables/jquery.dataTables.js'></script>";
    jsfilesText += "<script src='/static/vendor/datatables/dataTables.bootstrap4.js'></script>";
    jsfilesText += "<script src='/static/js/monitordata.js'></script>";
    /* 通过接口页面返回html,拼接给div */
    $.get("/monitor/data",function(data){
        $("#cssfiles").html(cssfilesText);
        $("#mainWeb").html(data);
        $("#jsfiles").html(jsfilesText);
        /* 判断页面select初始化结果,为select添加默认值 */
        var sss = $("#select_host_ip");
        if ( sss.length > 0 ) {
            sss.find("option:selected").removeAttr("selected");
            sss.append("<option data-hidden='true' disabled='disabled' selected='selected'> "
                + "Select Server To Search :D" + "</option>");
        }
        /* 载入server数据 */
        LoadWebFunc("server");
        $("#search_info").hide();
        /* bootstrap-select需要重新实例化 */
        $(".selectpicker").data('selectpicker',null).selectpicker();
    })
}
