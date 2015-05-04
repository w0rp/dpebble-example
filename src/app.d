import pebble;

nothrow
extern(C) int main(int argc, char **argv) {
    Window* window = window_create();
    scope(exit) window_destroy(window);

    window_set_click_config_provider(window, (context) {
        /+
        window_single_click_subscribe(BUTTON_ID_SELECT, (r, c) {
            text_layer_set_text(text_layer, "Select");
        });

        window_single_click_subscribe(BUTTON_ID_UP, (r, c) {
            text_layer_set_text(text_layer, "Up");
        });

        window_single_click_subscribe(BUTTON_ID_DOWN, (r, c) {
            text_layer_set_text(text_layer, "Down");
        });
        +/
    });

    WindowHandlers handlers;

    handlers.load = (window) {
        window_set_background_color(window, GColorScreaminGreen);

        /+
        Layer *window_layer = window_get_root_layer(window);
        GRect bounds = layer_get_bounds(window_layer);

        text_layer = text_layer_create(
            GRect(GPoint(0, 72), GSize(bounds.size.w, 20))
        );

        text_layer_set_text(text_layer, "Press a button");
        text_layer_set_text_alignment(text_layer, GTextAlignmentCenter);
        layer_add_child(window_layer, text_layer_get_layer(text_layer));
        +/
    };

    handlers.unload = (window) {
        /* text_layer_destroy(text_layer); */
    };

    window_set_window_handlers(window, handlers);

    const bool animated = true;
    window_stack_push(window, animated);

    /+APP_LOG(APP_LOG_LEVEL_DEBUG, "Done initializing, pushed window: %p", window);+/

    app_event_loop();

    return 0;
}

