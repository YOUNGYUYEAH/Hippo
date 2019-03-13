$(function(){
    $("#login_form").click(function(){
        $.ajax({
            url:"/login/",
            type: "POST",
            dataType: "json",
            data: {username:$("#username").val(), password:$("#password").val()}
        });
    });
});
