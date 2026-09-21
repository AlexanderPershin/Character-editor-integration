import pygame

import utils
from animation import Animation
from config import Config
from enemy import Enemy
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
        self.enemies = pygame.sprite.Group()

        self.player = Player(
            pygame.Vector2(
                self.config.window_width // 2, self.config.window_height // 2
            ),
            300,
            self.player_animations,
        )
        self.all_sprites.add(self.player, layer=5)

        enemy = Enemy(
            pygame.Vector2(self.screen_width, self.screen_height / 2),
            200,
            self.enemy_animations,
        )
        self.all_sprites.add(enemy, layer=4)
        self.enemies.add(enemy)

        self.running = True

        return self

    def __exit__(self, *args):
        pygame.quit()

    def _load_font(self) -> None:
        self.font = pygame.font.Font(
            self.config.font_path, self.config.gui_font_size
        )

    def _load_images(self) -> None:
        self.player_animations = utils.load_animations("assets/player_animations.json")
        self.enemy_animations = utils.load_animations("assets/enemy_animations.json")

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
        self.all_sprites.update(self.dt, target=self.player)

    def draw(self):
        self.screen.fill(self.config.bg_color)

        self.all_sprites.draw(self.screen)

        pygame.display.flip()
