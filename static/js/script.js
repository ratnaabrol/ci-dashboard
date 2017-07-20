timer = setInterval(function(){updateDashboard();}, parseInt(interval));

$(document).ready(function(){
    
    updateDashboard(); 
    $("#actions").on("shown.bs.modal", function (e) {
        clearTimeout(timer);
        var slug = e.relatedTarget.dataset.slug; 
        $.ajax({
            url: "/modal?slug=" + slug,
            success: function (data) {
                $('.modal-content').html(data);
            },
        });      
    });

    $("#actions").on("hidden.bs.modal", function(event){
        $('.modal-content').html('<div class="modal-loading">Loading...</div>');
        timer = setInterval(function(){updateDashboard();}, parseInt(interval));
    });

    $("#event_filter").change(function() {
        updateDashboard();
    });

});

function updateDashboard(){
    $("#update-loader").show();
   var event_type = $('#event_filter').val();
    $.ajax({
        url: "/dashboard/update?event_type=" + event_type,
        success: function (data) {
           $('#container').html(data);
           $("#update-loader").hide();
        }
    });
};

function filter_events(event)
{
    if (event == 'all'){
        $("#event_filter").text('Events');
    }
    else{
        $("#event_filter").text("Event : " + event.replace('_', ' '));
    }
   
   $("#event_filter").val(event);
   updateDashboard();
}

