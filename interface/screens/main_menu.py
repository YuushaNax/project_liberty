import pygame as pg

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        # ✅ Crear fuentes aquí (después de pg.init())
        self.font = pg.font.SysFont("consolas", 32)
        self.title_font = pg.font.SysFont("arial", 72)
        self.options = ["Nueva Partida", "Cargar Partida", "Salir"]
        self.selected = 0

    def draw_centered_text(self, text, font, color, y):
        text_surface = font.render(text, True, color)
        x = self.screen.get_width() // 2 - text_surface.get_width() // 2
        self.screen.blit(text_surface, (x, y))

    def run(self):
        clock = pg.time.Clock()
        WHITE = (255, 255, 255)
        GRAY = (180, 180, 180)
        HIGHLIGHT = (100, 200, 255)
        BLACK = (10, 10, 10)

        while True:
            self.screen.fill(BLACK)
            self.draw_centered_text("PROJECT LIBERTY", self.title_font, WHITE, 150)

            for i, opt in enumerate(self.options):
                color = HIGHLIGHT if i == self.selected else GRAY
                self.draw_centered_text(opt, self.font, color, 350 + i * 80)

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pg.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key in (pg.K_RETURN, pg.K_SPACE):
                        return self.options[self.selected]

            clock.tick(30)
