
function dashboardUpdateService() {
    this.monitoringTimer = null;

    this.begin = function(currentPage, numberOfRepos, gridSize, interval) {
        this.currentPage = currentPage;
        this.numberOfRepos = numberOfRepos;
        this.gridSize = gridSize;
        this.numberOfPages = Math.ceil(this.numberOfRepos / this.gridSize);
        this.interval = interval;
        this.startTimer();        
    };

    this.startTimer = function() {
        if(this.monitoringTimer) {return}
        var _this = this;
        this.monitoringTimer = setInterval(function() {
            _this.updateHandller()} , this.interval);
    }

    this.stopTimer = function() {
        clearInterval(this.monitoringTimer);
        this.monitoringTimer = null;
    };

    this.pagination = function() {
        if(this.currentPage > this.numberOfPages){
            this.currentPage = 1;
        }
        var start = this.gridSize * (this.currentPage - 1);
        if ((start + this.gridSize) < this.numberOfRepos) {
            end = start + this.gridSize - 1;
        }
        else {
            end = this.numberOfRepos-1;
        }
        return [start, end];
    }

    this.updateHandller = function() {
        var [start, end] = this.pagination();
        $.ajax({
            url: "/dashboard/update?start=" + start + "&end=" + end,
            success: function (data) {
                $('#page').html(data);
            }
        });

        this.currentPage++;
    }
}

updateService = new dashboardUpdateService();












// 

// function dashboardUpdateHandller(interval, pages){
//     currentPage = 1;
//     numberOfPages = pages;
//     startMonitoringService(interval);
// }

// function startMonitoringService(interval){
//     if(monitoringTimer){
//         return
//     }
//     monitoringTimer = setInterval(function(){
//         updateDashboard()}, interval);
// }
    
// function stopMonitoringService(){
//     clearInterval(monitoringTimer);
//     monitoringTimer = null;
// }

// function updateDashboard(){
//     if(currentPage > numberOfPages){
//         currentPage = 1
//     }
//     $('#page').html(currentPage);
    // currentPage++;
// };






// $(document).ready(function(){
    
//     updateDashboard(); 
//     $("#actions").on("shown.bs.modal", function (e) {
//         clearTimeout(timer);
//         var slug = e.relatedTarget.dataset.slug; 
//         $.ajax({
//             url: "/dashboard/modal?slug=" + slug,
//             success: function (data) {
//                 $('.modal-content').html(data);
//             },
//         });      
//     });

//     $("#actions").on("hidden.bs.modal", function(event){
//         $('.modal-content').html('<div class="modal-loading">Loading...</div>');
//         timer = setInterval(function(){updateDashboard();}, parseInt(interval));
//     });

//     $("#event_filter").change(function() {
//         updateDashboard();
//     });

// });

// function updateDashboard(){
//     $("#update-loader").show();
//    var event_type = $('#event_filter').val();
//     $.ajax({
//         url: "/dashboard/update?event_type=" + event_type,
//         success: function (data) {
//            $('#container').html(data);
//            $("#update-loader").hide();
//         }
//     });
// };
