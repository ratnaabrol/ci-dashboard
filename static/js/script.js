xhr = null;

function startDashboardService() {
    _dashboardService = new dashboardService();
    _dashboardService.updateDashboard();
}

function dashboardService() {
    service = this;
    service.timer = null;
    service.currentPage = 1;
    service.eventType = null;
    service.interval = interval;
    service.requestData = Object();

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
        service.requestData = Object();
    };

    service.updateDashboard = function() {

        service.requestData.page = service.currentPage;
        if(service.eventType) {
            service.requestData.event_type = service.eventType;
        }

        if(xhr){xhr.abort();}

        xhr = $.ajax({
            url: '/dashboard/fetch',
            data: service.requestData,
            beforeSend: function() {
                service.stop();
                $("#update-loader").show();
            },
            success: function(data, status, xhr) {
                $('#container').html(data);
                $('#pagination').html('Page ' +  service.currentPage + ' of ' + xhr.getResponseHeader('pages'));
                
                if (xhr.getResponseHeader('last_page') == 'True') {
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

    //event filter
    $('#eventFilter li').on('click', function() {
        var event = $(this).attr('event');
        if(event == 'all') {
            $("#filterLabel").html('Events');
            _dashboardService.eventType = null;
        }
        else {
             $("#filterLabel").html("Events : " + $(this).text());
            _dashboardService.eventType = event;
        }
        _dashboardService.reset();
        _dashboardService.updateDashboard();
    });
});



