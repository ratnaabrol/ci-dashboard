xhr = null;

function startDashboardService() {
    _dashboardService = new dashboardService();
    _dashboardService.updateDashboard();
}

function dashboardService() {
    service = this;
    service.timer = null;
    service.currentPage = 1;
    service.interval = interval;

    service.start = function() {
        if(service.timer) {return;}
        service.timer = setInterval(function(){
            service.updateDashboard()} , service.interval);
    };

    service.stop = function() {
        if(!service.timer) {return;}
        clearInterval(service.timer);
        service.timer = null;
    };

    service.reset = function() {
        service.currentPage = 1;
    };

    service.updateDashboard = function() {

        var requestUrl = "/dashboard/fetch?page=" + service.currentPage;
        eventType = $("#eventFilter").val(); 

        if(eventType) {
            requestUrl += "&event_type=" + eventType;
        }

        xhr = $.ajax({
            url: requestUrl,
            beforeSend: function() {
                service.stop();
                $("#update-loader").show();
            },
            success: function(data, status, xhr) {
                var lastPage = xhr.getResponseHeader('last_page');
                var number_of_pages = xhr.getResponseHeader('pages');
                $('#pagination').html(service.currentPage+'/'+number_of_pages);
                $('#container').html(data);
                if (lastPage == 'True') {
                    service.currentPage = 1;
                }
                else {
                    service.currentPage++;
                } 
            },
            complete: function() {
                service.start();
                $("#update-loader").hide();
            }
         }); 
    }
}

function filterEvents(event) {
    if (event == 'all') {
        $("#eventFilter").textEvents('');
    }
    else {
        $("#eventFilter").text("Event : " + event.replace('_', ' '));
    }

    $("#eventFilter").val(event);

    _dashboardService.reset();
    _dashboardService.updateDashboard();
}



$(document).ready(function(){  
    //show modal  
    $("#modal").on("shown.bs.modal", function (e) {
        _dashboardService.stop();
        var slug = e.relatedTarget.dataset.slug; 
        $.ajax({
            url: "/dashboard/modal?slug=" + slug,
            success: function (data) {
                $('.modal-content').html(data);
            },
            error: function(data) {
                var errorMsg = 'Unexpected error: ' + data.statusText;
                $('.modal-content').html(errorMsg);
            }
        });      
    });
    //hide modal
    $("#modal").on("hidden.bs.modal", function(event){
        $('.modal-content').html('<div class="modal-loading">Loading...</div>');
        _dashboardService.start();
    });
});




