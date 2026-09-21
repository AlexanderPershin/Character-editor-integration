import math
import pygame

import utils
from animation import Animation

JUMP_HEIGHT = 128 

class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: pygame.Vector2,
        speed: int,
        animations: dict[str, Animation],
        gravity: float = 2000.0,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.animations = animations
        self.current_anim_name = "idle"
        self.last_anim_name = "idle"

        self.speed = speed
        self.pos = pos

        self.gravity = gravity
        self.vel_y = 0.0
        self.is_airborne = False
        self.ground_y = pos.y

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def play(self, name: str) -> None:
        if name != self.last_anim_name:
            self.animations[name].reset()
            self.last_anim_name = name
        self.current_anim_name = name


    def _start_jump(self) -> None:
        self.vel_y = -math.sqrt(2.0 * self.gravity * JUMP_HEIGHT)
        self.is_airborne = True
        self.ground_y = self.pos.y

    def update(self, dt: float, *args, **kwargs) -> None:
        keys = pygame.key.get_pressed()
        mouse_btns = pygame.mouse.get_pressed()

        move = utils.get_movement_direction(keys)

        direction = "down"
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction = "up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction = "down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction = "right"

        is_running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        is_jump_pressed = keys[pygame.K_SPACE]

        speed = self.speed
        if is_running:
            speed *= 2

        self.pos += move * speed * dt

        if is_jump_pressed and not self.is_airborne:
            self._start_jump()

        if self.is_airborne:
            self.vel_y += self.gravity * dt
            self.pos.y += self.vel_y * dt
            if self.pos.y >= self.ground_y:
                self.pos.y = self.ground_y
                self.vel_y = 0.0
                self.is_airborne = False
        else:
            self.ground_y = self.pos.y

        self.rect.center = self.pos

        is_moving = move.length_squared() > 0
        is_attack = mouse_btns[0]
        is_backlash = mouse_btns[2]
        is_spellcast = keys[pygame.K_f]

        if self.is_airborne:
            new_anim_name = "jump"
        elif is_backlash:
            new_anim_name = "backlash"
        elif is_attack:
            new_anim_name = "slash"
        elif is_moving and is_running:
            new_anim_name = "run"
        elif is_moving and not is_running:
            if is_spellcast:
                new_anim_name = "spellcast"
            else:
                new_anim_name = "walk"
        else:
            if is_spellcast:
                new_anim_name = "spellcast"
            else:
                new_anim_name = "idle"


        self.play(new_anim_name)

        anim = self.animations[self.current_anim_name]
        if is_moving:
            anim.set_direction(direction)

        frame = anim.update(dt)
        if frame is not None:
            self.image = frame
            self.rect = self.image.get_rect(center=self.pos)
            self.mask = pygame.mask.from_surface(self.image)
