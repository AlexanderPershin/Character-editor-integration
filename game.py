import pygame

import utils
from animation import Animation
from config import Config
from player import Player


class Game:
    def __init__(self, config: Config):
        self.running = False
        self.config = config

    def __enter__(self):
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512,
            allowedchanges=pygame.AUDIO_ALLOW_ANY_CHANGE,
        )

        pygame.init()

        pygame.mixer.set_num_channels(16)

        self.screen = pygame.display.set_mode((self.config.window_width, self.config.window_height))

        self.screen_width, self.screen_height = self.screen.get_size()
        self.screen_rect = self.screen.get_rect()

        pygame.display.set_caption("Character Generator")

        self.clock = pygame.time.Clock()

        self._load_font()
        self._load_images()
        self._load_sounds()

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.player_animations = {
            "idle": Animation(self.player_idle_frames, 150),
            "walk": Animation(self.player_walk_frames, 150),
            "run": Animation(self.player_run_frames, 150),
            "jump": Animation(self.player_jump_frames, 150),
            "slash": Animation(self.player_slash_frames, 25),
            "backlash": Animation(self.player_backslash_frames, 25),
            "spellcast": Animation(self.player_spellcast_frames, 25),
        }

        self.player = Player(
            pygame.Vector2(
                self.config.window_width // 2, self.config.window_height // 2
            ),
            300,
            self.player_animations,
        )
        self.all_sprites.add(self.player, layer=5)

        self.running = True

        return self

    def __exit__(self, *args):
        pygame.quit()

    def _load_font(self) -> None:
        self.font = pygame.font.Font(
            self.config.font_path, self.config.gui_font_size
        )

    def _load_images(self) -> None:
        player_sprite_sheet_idle = pygame.image.load(
            "images/idle.png"
        ).convert_alpha()

        self.player_idle_frames = utils.load_sprite_frames(
            player_sprite_sheet_idle, 64, 64, frame_count=2, rows=4
        )

        player_sprite_sheet_walk = pygame.image.load(
            "images/walk.png"
        ).convert_alpha()

        self.player_walk_frames = utils.load_sprite_frames(
            player_sprite_sheet_walk, 64, 64, frame_count=9, rows=4
        )

        player_sprite_sheet_run = pygame.image.load(
            "images/run.png"
        ).convert_alpha()

        self.player_run_frames = utils.load_sprite_frames(
            player_sprite_sheet_run, 64, 64, frame_count=8, rows=4
        )

        player_sprite_sheet_jump = pygame.image.load(
            "images/jump.png"
        ).convert_alpha()

        self.player_jump_frames = utils.load_sprite_frames(
            player_sprite_sheet_jump, 64, 64, frame_count=5, rows=4
        )

        player_sprite_sheet_slash = pygame.image.load(
            "images/slash_128.png"
        ).convert_alpha()

        self.player_slash_frames = utils.load_sprite_frames(
            player_sprite_sheet_slash, 128, 128, frame_count=6, rows=4
        )

        player_sprite_sheet_backslash = pygame.image.load(
            "images/backslash_128.png"
        ).convert_alpha()

        self.player_backslash_frames = utils.load_sprite_frames(
            player_sprite_sheet_backslash, 128, 128, frame_count=13, rows=4
        )

        player_sprite_sheet_spellcast = pygame.image.load(
            "images/spellcast.png"
        ).convert_alpha()

        self.player_spellcast_frames = utils.load_sprite_frames(
            player_sprite_sheet_spellcast, 64, 64, frame_count=7, rows=4
        )

    def _load_sounds(self) -> None:
        pass

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.config.fps) / 1000
            self.watch_for_events()
            self.update()
            self.draw()

    def watch_for_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

    def update(self):
        self.all_sprites.update(self.dt)

    def draw(self):
        self.screen.fill(self.config.bg_color)

        self.all_sprites.draw(self.screen)

        pygame.display.flip()
