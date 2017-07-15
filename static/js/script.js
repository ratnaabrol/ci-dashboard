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

});

function updateDashboard(){
    $.ajax({
        url: "/update",
        success: function (data) {
           $('#container').html(data);
        }
    });
};

