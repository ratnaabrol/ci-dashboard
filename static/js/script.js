xhr = null;

function startDashboardUpdateService(currentPage) {
    updateService = new dashboardUpdateService(currentPage);
    updateService.updateNow();
    updateService.run();
}

function dashboardUpdateService(currentPage) {
    this.monitoringTimer = null;
    this.currentPage = currentPage;
    this.numberOfPages = Math.ceil(numberOfRepos / gridSize);

    this.run = function() {
        if(this.monitoringTimer) {
            return
        }
        var _this = this;
        this.monitoringTimer = setInterval(function() {
            _this.updateNow()} , interval);
    }

    this.pause = function() {
        clearInterval(this.monitoringTimer);
        this.monitoringTimer = null;
    };

    this.pagination = function() { 
        if(this.currentPage > this.numberOfPages){
            this.currentPage = 1;
        }
        var start = gridSize * (this.currentPage - 1);
        if ((start + gridSize) < numberOfRepos) {
            end = start + gridSize;
        }
        else {
            end = numberOfRepos;
        }
        return [start, end];
    }

    this.updateNow = function() {
        if(xhr){
            xhr.abort()
        }
        var [start, end] = this.pagination();
        var event_type = $("#eventFilter").val();
        xhr = $.ajax({
            url: "/dashboard/update?start="+start+"&end="+end+"&event_type="+event_type,
            beforeSend: function() {
                $("#update-loader").show();
            },
            success: function(data) {
                $('#container').html(data);
            },
            complete: function() {
                $("#update-loader").hide();
            }
        });
        
        this.currentPage++;
    }
}

$(document).ready(function(){  
    //show modal  
    $("#modal").on("shown.bs.modal", function (e) {
        updateService.pause();
        var slug = e.relatedTarget.dataset.slug; 
        $.ajax({
            url: "/dashboard/modal?slug=" + slug,
            success: function (data) {
                $('.modal-content').html(data);
            }
        });      
    });
    //hide modal
    $("#modal").on("hidden.bs.modal", function(event){
        $('.modal-content').html('<div class="modal-loading">Loading...</div>');
        updateService.run();
    });

});


function filterEvents(event) {
    if (event == 'all') {
        $("#eventFilter").text('Events');
    }
    else {
        $("#eventFilter").text("Event : " + event.replace('_', ' '));
    }
   $("#eventFilter").val(event);
   updateService.currentPage = 1;
   updateService.updateNow();
}