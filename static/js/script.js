function resizePanelItems(){
    var panel_head_height = 0.23;
    var panel_content_height = 0.56;
    var panel_footer_height = 0.21;
    var event_details_height = 0.16*0.56;
    var panel_height = parseInt($(".panel").height());
    var repo_title_size = panel_height*panel_head_height*0.47;
    var event_title_size = panel_height*panel_content_height*0.16;
    var event_details_text_size = panel_height*event_details_height*0.95;
    var event_details_img_size = panel_height*event_details_height;
    var event_details_margin = panel_height*event_details_height*0.6;
    var panel_footer_text = panel_height*panel_footer_height*0.35;

    $(".panel-head a").css('font-size', repo_title_size);
    $(".panel-content .event-title").css('font-size', event_title_size);
    $(".event-details p").css('font-size', event_details_text_size);
    $(".event-details img").css('width', event_details_img_size);
    $(".event-details").css('margin', event_details_margin);
    $(".panel-footer a").css('font-size', panel_footer_text);
}