# interface/screens/create_player.py
import pygame as pg
import json
import random
import os
from pathlib import Path
from .base_screen import BaseScreen
from .text_input import TextInput
from engine.entities.entity import Entity

# === CONFIGURACIÓN DE INTERFAZ ===
# Nota: asumimos pg.init() y display ya inicializados antes de instanciar pantallas
FONT = pg.font.SysFont("consolas", 32)
TITLE = pg.font.SysFont("arial", 64)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
HIGHLIGHT = (100, 200, 255)
GREEN = (100, 255, 100)
BLACK = (10, 10, 10)

# === RUTAS BASE ===
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA = BASE_DIR / "data"
GAMES = BASE_DIR / "saves" / "games"


def draw_centered(surface, text, font, color, y):
    """Dibuja texto centrado horizontalmente."""
    s = font.render(str(text), True, color)
    x = surface.get_width() // 2 - s.get_width() // 2
    surface.blit(s, (x, y))


def wrap_text(text, max_width, font):
    """Wrap text to fit within max_width and return list of lines."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        text_surf = font.render(test_line, True, WHITE)
        if text_surf.get_width() < max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return lines


class CreatePlayer(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.phase = "name"
        # clock used by modal summary and other waits
        self.clock = pg.time.Clock()

        # Cargar data desde JSON
        with open(DATA / "races.json", encoding="utf-8") as f:
            self.races = json.load(f)
        with open(DATA / "stats.json", encoding="utf-8") as f:
            self.stats_data = json.load(f)

        self.name = ""
        self.age = 0
        self.selected_race = None
        self.race_index = 0
        self.maturity_age = 18  # Default, will be set from race
        
        # Childhood events selection
        with open(DATA / "childhood_events.json", encoding="utf-8") as f:
            self.childhood_data = json.load(f)

        # Childhood progression tracking
        self.available_events = []
        self.event_index = 0
        self.selected_event = None
        self.option_index = 0
        self.selected_option = None
        self.childhood_history = []  # Track all selected events and their effects
        
        # Store stats for use in childhood event phase
        self.stats = None
        
        # Age progression tracker
        self.age_progression_index = 0  # Which age category we're in (0=birth, 1=age_1_2, etc.)

    # -----------------------
    # Manejo de eventos (llamado por BaseScreen.run)
    # -----------------------
    def handle_event(self, event):
        # Para fases que no dependen de texto modal, aceptamos input directo
        if self.phase == "race":
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.race_index = (self.race_index - 1) % len(self.races)
                elif event.key == pg.K_DOWN:
                    self.race_index = (self.race_index + 1) % len(self.races)
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    self.selected_race = self.races[self.race_index]
                    # Set maturity age from race
                    self.maturity_age = int(self.selected_race.get("maturity", 18))
                    self.age = 0  # Start at age 0
                    # Initialize base stats (from race and stats_data)
                    self._init_stats()
                    # Prepare first childhood events (birth)
                    self._prepare_next_childhood_events()
                    self.phase = "childhood"

        # En las demás fases no procesamos aquí porque usan TextInput modal o resumen
        elif self.phase == "finalize":
            # permitir cancelar con ESC si lo quieres (ejemplo)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
        elif self.phase == "childhood":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.event_index = (self.event_index - 1) % max(1, len(self.available_events))
                elif event.key == pg.K_DOWN:
                    self.event_index = (self.event_index + 1) % max(1, len(self.available_events))
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    # select event and go to option selection (if options exist)
                    self.selected_event = self.available_events[self.event_index]
                    # if event has options, go to option phase, otherwise apply and continue
                    opts = self.selected_event.get("options") or []
                    if opts:
                        self.phase = "childhood_option"
                        self.option_index = 0
                    else:
                        self.selected_option = None
                        # Apply event with no option and progress
                        self._progress_to_next_age()
        elif self.phase == "childhood_option":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.option_index = (self.option_index - 1) % max(1, len(self.selected_event.get("options", [])))
                elif event.key == pg.K_DOWN:
                    self.option_index = (self.option_index + 1) % max(1, len(self.selected_event.get("options", [])))
                elif event.key in (pg.K_RETURN, pg.K_SPACE):
                    self.selected_option = self.selected_event.get("options", [])[self.option_index]
                    # Apply effects and move to next age
                    self._progress_to_next_age()

    # ===============================
    # BUCLE PRINCIPAL DE ACTUALIZACIÓN
    # ===============================
    def update(self):
        # Las fases que necesitan texto usan TextInput (modal)
        if self.phase == "name":
            inp = TextInput(self.screen, "Nombre del personaje:")
            inp.run()
            # si el usuario canceló (entrada vacía), volvemos al menú
            if not inp.result:
                self.running = False
                return
            self.name = inp.result
            self.phase = "race"

        elif self.phase == "race":
            # aquí solo hacemos lógica por frame si hace falta (por ahora nada)
            pass

        elif self.phase == "finalize":
            self.save_player()
            self.show_summary()
            self.running = False

    def _prepare_next_childhood_events(self):
        """Prepare childhood events for the current age.
        Maps age to appropriate category and loads events.
        """
        # Age categories mapping
        age_categories = [
            (0, "birth"),
            (1, "age_1_2"),
            (3, "age_3_5"),
            (6, "age_6_10"),
            (11, "age_11_15"),
            (16, "age_16_20"),
        ]
        
        # Find the appropriate category for current age
        current_category = None
        for threshold_age, category_name in age_categories:
            if self.age >= threshold_age:
                current_category = category_name
        
        # Load events from the appropriate category
        if current_category and current_category in self.childhood_data:
            events = self.childhood_data.get(current_category, [])
            
            # Filter events by rareness: randomly include each event
            self.available_events = []
            for event in events:
                rareness = event.get("rareness", 0.5)
                if random.random() < rareness:
                    self.available_events.append(event)
            
            # Ensure we have at least 1 event; if not, pick a random one
            if not self.available_events and events:
                self.available_events = [random.choice(events)]
        else:
            self.available_events = []
        
        # Always include special events as an option
        special_events = self.childhood_data.get("special_events", [])
        if special_events:
            for event in special_events:
                rareness = event.get("rareness", 0.5)
                if random.random() < rareness:
                    self.available_events.append(event)
        
        self.event_index = 0
        self.selected_event = None
        self.option_index = 0

    def _progress_to_next_age(self):
        """Apply selected option effects and progress to next age category or finish."""
        # Apply the selected option effects
        self._apply_selected_option()
        
        # Increment age
        self.age += 1
        
        if self.age >= self.maturity_age:
            # Reached maturity, finish creation
            self.phase = "finalize"
        else:
            # Move to next age category
            self._prepare_next_childhood_events()
            if not self.available_events:
                # No more events available, finish
                self.phase = "finalize"
            else:
                # Reset event index for new age category
                self.event_index = 0
                self.selected_event = None
                self.selected_option = None
                self.phase = "childhood"

    def _apply_selected_option(self):
        """Apply the selected option's effects to stats and record in history."""
        if self.selected_event and self.selected_option:
            effects = self.selected_option.get("effect", {})
            for stat_name, delta in effects.items():
                if stat_name in self.stats:
                    try:
                        self.stats[stat_name] += int(delta)
                    except Exception:
                        self.stats[stat_name] += float(delta)
            
            # Record in history
            self.childhood_history.append({
                "age": self.age,
                "event_name": self.selected_event.get("event_name"),
                "option_name": self.selected_option.get("option_name"),
                "effects": effects
            })

    def _prepare_childhood_events(self):
        """DEPRECATED: Kept for backwards compatibility with tests.
        Use _prepare_next_childhood_events instead.
        """
        self._prepare_next_childhood_events()

    def _init_stats(self):
        """Initialize `self.stats` from `self.stats_data` and apply race modifiers.
        This ensures stats exist before childhood events modify them.
        """
        # base stats
        self.stats = {s["stat_name"]: 10 for s in self.stats_data}
        # apply race modifiers if available
        if self.selected_race:
            for mod in self.selected_race.get("modifiers", []):
                stat_name = mod.get("stat_name")
                modifier = mod.get("modifier", 0)
                if stat_name in self.stats:
                    try:
                        self.stats[stat_name] += int(modifier)
                    except Exception:
                        self.stats[stat_name] += float(modifier)

    # ===============================
    # DIBUJADO POR FASE
    # ===============================
    def draw(self):
        # improved visual: dark background + centered panel
        self.screen.fill((18, 18, 20))
        panel_w, panel_h = self.screen.get_width() - 200, self.screen.get_height() - 200
        panel = pg.Surface((panel_w, panel_h))
        panel.fill((26, 26, 30))
        panel_rect = panel.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        # panel border
        pg.draw.rect(self.screen, (60, 60, 70), panel_rect.inflate(6, 6))
        self.screen.blit(panel, panel_rect)

        title_y = panel_rect.top + 40
        if self.phase == "race":
            draw_centered(self.screen, "Selecciona tu raza:", TITLE, WHITE, title_y)
            # dibujar un máximo de N items en pantalla si hay muchas razas
            list_y = title_y + 120
            for i, race in enumerate(self.races):
                color = HIGHLIGHT if i == self.race_index else GRAY
                draw_centered(self.screen, race.get("display", f"race_{i}"), FONT, color, list_y + i * 56)

        elif self.phase == "childhood":
            draw_centered(self.screen, f"Tu infancia - Edad {self.age} ({self.age}/{self.maturity_age})", TITLE, WHITE, title_y)
            
            if not self.available_events:
                list_y = title_y + 120
                draw_centered(self.screen, "No hay eventos disponibles.", FONT, GRAY, list_y)
            else:
                # Left column: event list
                list_y = title_y + 120
                list_item_height = 50
                max_visible_events = 3
                
                for i, ev in enumerate(self.available_events[:max_visible_events]):
                    display = ev.get("event_name", f"evento_{i}")
                    color = HIGHLIGHT if i == self.event_index else GRAY
                    draw_centered(self.screen, display, FONT, color, list_y + i * list_item_height)
                
                # Right column: event description with wrapping
                if self.event_index < len(self.available_events):
                    sel = self.available_events[self.event_index]
                    desc = sel.get("description", "")
                    rareness = sel.get("rareness", 0)
                    
                    # Wrap description
                    desc_max_width = panel_w - 200
                    wrapped_lines = wrap_text(desc, desc_max_width, FONT)
                    
                    desc_y = list_y
                    small_font = pg.font.SysFont("consolas", 24)
                    draw_centered(self.screen, "Descripción:", small_font, WHITE, desc_y)
                    
                    for line_idx, line in enumerate(wrapped_lines[:4]):  # Limit to 4 lines
                        draw_centered(self.screen, line, small_font, GRAY, desc_y + 35 + line_idx * 28)
                    
                    # Show rarity
                    rarity_text = f"Probabilidad: {int(rareness * 100)}%"
                    draw_centered(self.screen, rarity_text, small_font, (150, 150, 255), desc_y + 150)
                
                # Show childhood history on bottom
                if self.childhood_history:
                    history_y = panel_rect.bottom - 100
                    draw_centered(self.screen, "Tu historia hasta ahora:", small_font, GRAY, history_y)
                    for i, past_event in enumerate(self.childhood_history[-2:]):  # Show last 2 events
                        history_text = f"Edad {past_event['age']}: {past_event['event_name']}"
                        draw_centered(self.screen, history_text, pg.font.SysFont("consolas", 20), GRAY, history_y + 30 + i * 25)

        elif self.phase == "childhood_option":
            draw_centered(self.screen, "Selecciona opción del evento:", TITLE, WHITE, title_y)
            list_y = title_y + 120
            opts = self.selected_event.get("options", []) if self.selected_event else []
            option_height = 60
            
            for i, opt in enumerate(opts):
                text = opt.get("option_name", f"op_{i}")
                color = HIGHLIGHT if i == self.option_index else GRAY
                draw_centered(self.screen, text, FONT, color, list_y + i * option_height)
            
            # Show effect preview with wrapping
            if opts:
                eff = opts[self.option_index].get("effect", {})
                eff_text = "Efectos: "
                for stat, value in eff.items():
                    symbol = "+" if value > 0 else ""
                    eff_text += f"{stat} {symbol}{value}, "
                eff_text = eff_text.rstrip(", ")
                
                # Wrap effect text
                effect_max_width = panel_w - 200
                wrapped_effects = wrap_text(eff_text, effect_max_width, FONT)
                
                effect_y = list_y + len(opts) * option_height + 40
                for line_idx, line in enumerate(wrapped_effects[:2]):
                    small_eff_font = pg.font.SysFont("consolas", 26)
                    draw_centered(self.screen, line, small_eff_font, GRAY, effect_y + line_idx * 30)

        elif self.phase == "finalize":
            draw_centered(self.screen, "Creando personaje...", FONT, WHITE, title_y + 200)

    # ===============================
    # GUARDADO Y RESUMEN
    # ===============================
    def save_player(self):
        # prefer the in-memory stats (which include childhood effects), fallback to default
        stats = getattr(self, "stats", {s["stat_name"]: 10 for s in self.stats_data})

        player = Entity(
            name=self.name,
            new_stats=stats,
            height=random.randint(
                int(self.selected_race.get("min_height", 150)),
                int(self.selected_race.get("max_height", 190)),
            ),
        )
        player.race = {self.selected_race.get("race_name", self.selected_race.get("display")): 100}
        player.age = self.age

        os.makedirs(GAMES, exist_ok=True)
        path = GAMES / f"{self.name.lower().replace(' ', '_')}.json"

        # Include full childhood history in save
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "name": player.name,
                    "race": player.race,
                    "age": player.age,
                    "stats": player.stats,
                    "height": player.height,
                    "childhood_journey": self.childhood_history,
                },
                f,
                indent=4,
            )

    def show_summary(self):
        waiting = True
        while waiting:
            self.screen.fill(BLACK)
            draw_centered(self.screen, "✅ PERSONAJE CREADO", TITLE, GREEN, 100)
            draw_centered(self.screen, f"Nombre: {self.name}", FONT, WHITE, 250)
            draw_centered(
                self.screen, f"Raza: {self.selected_race.get('display','?')}", FONT, WHITE, 300
            )
            draw_centered(self.screen, f"Edad: {self.age}", FONT, WHITE, 350)
            
            # Show childhood journey summary
            small_font = pg.font.SysFont("consolas", 24)
            draw_centered(self.screen, "Tu viaje de infancia:", small_font, WHITE, 420)
            
            if self.childhood_history:
                history_y = 460
                for event_info in self.childhood_history[-5:]:  # Show last 5 events
                    event_text = f"Edad {event_info['age']}: {event_info['event_name']} → {event_info['option_name']}"
                    draw_centered(self.screen, event_text, pg.font.SysFont("consolas", 18), GRAY, history_y)
                    history_y += 28
            else:
                draw_centered(self.screen, "Sin eventos registrados", small_font, GRAY, 460)
            
            draw_centered(self.screen, "Presiona ENTER para continuar", FONT, GRAY, 650)

            pg.display.flip()
            self.clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    waiting = False
