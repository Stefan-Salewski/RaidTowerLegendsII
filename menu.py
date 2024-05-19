def menu(SCREEN_WIDTH, SCREEN_HEIGHT, clock, colours, screen, fonts):
    # RENDER YOUR GAME HERE
    REGULAR_FONT = fonts[0]
    TITLE_FONT = fonts[1]
    title_display = TITLE_FONT.render("Raid Tower Legends II", True, colours[0])

    screen.blit(title_display, (SCREEN_WIDTH / 2 - title_display.get_width() / 2, 100))

    # debug
    version = REGULAR_FONT.render("0.0.1", True, colours[0])
    screen.blit(version, (SCREEN_WIDTH - version.get_width(), SCREEN_HEIGHT - version.get_height()))

    fps_counter = REGULAR_FONT.render(str(round(clock.get_fps(), 1)), True, colours[0])
    screen.blit(fps_counter, (0, 0))