$("#monitordata_cpu").click(function() {
    $("#monitorSubweb").load("/monitor/cpu");
});
$("#monitordata_disk").click(function(){
    $("#monitorSubweb").load("/monitor/disk");
});
$("#monitordata_memory").click(function(){
    $("#monitorSubweb").load("/monitor/memory");
});
