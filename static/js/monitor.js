$("#monitordata_cpu").click(function(){
    $("#monitorSubweb").load("/monitor/cpu");
});
$("#monitordata_memory").click(function(){
    $("#monitorSubweb").load("/monitor/memory",function(){
        $("#memoryunit").change(function(){
            var unit = $(this).val();
            $.ajax({
                url: '/monitor/memory',
                data: {'unit':unit},
                async: false,
                success: function(xhr){
                    if(xhr.status = 200) {
                        alert(data)
                    }
                }
            })
        })
    });
});