// update dashboard data
function updateDashboard(){
    $.ajax({
        url: "/update",
        success: function (data) {
           $('#container').html(data);
        },
    });
};

$(document).ready(function(){

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
        timer = setInterval(function(){updateDashboard();}, 5000);
    });

});