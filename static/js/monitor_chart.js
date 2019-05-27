$("#createchart_btn").click(function(){
    $.ajax({
        url: '/monitor/c',
        type: 'POST',
        cache: false,
        data: {'ip': "192.168.80.99",
            'type':"cpu",
            'time_start':"",
            'time_end':""
        },
        success: function(data, statsText, xhr) {
            if ( xhr.status === 200) {
                alert("ok");
            }
        },
    })
});

function Echarts(){
    
}