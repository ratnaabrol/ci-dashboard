function resizePanelItems(){
    var panel_top_height = 0.23;
    var panel_middle_height = 0.56;
    var panel_bottom_height = 0.21;
    var event_details_height = 0.16*0.56;
    var panel_height = parseInt($(".panel").height());
    var repo_title_size = panel_height*panel_top_height*0.47;
    var event_title_size = panel_height*panel_middle_height*0.16;
    var event_details_text_size = panel_height*event_details_height*0.95;
    var event_details_img_size = panel_height*event_details_height;
    var event_details_margin = panel_height*event_details_height*0.6;
    var panel_bottom_text = panel_height*panel_bottom_height*0.37;

    $(".panel-top a").css('font-size', repo_title_size);
    $(".panel-middle .event-title").css('font-size', event_title_size);
    $(".event-details p").css('font-size', event_details_text_size);
    $(".event-details img").css('width', event_details_img_size);
    $(".event-details").css('margin', event_details_margin);
    $(".panel-bottom a").css('font-size', panel_bottom_text);
    $(".panel-bottom p").css('font-size', panel_bottom_text);
}

$(window).resize(function () {
    resizePanelItems();
});