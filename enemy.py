from enum import StrEnum
from typing import Mapping

import pygame

from animation import Animation
from player import Direction, Player


class EnemyAnim(StrEnum):
    RUN = "run"
    ATTACK = "attack"


class Enemy(pygame.sprite.Sprite):
    def __init__(
            self,
            pos: pygame.Vector2,
            speed: int,
            animations: Mapping[EnemyAnim, Animation],
            attack_range: float = 78.0,
    ) -> None:
        super().__init__()

        self.animations = animations
        self.current_anim = EnemyAnim.RUN
        self.speed = speed
        self.pos = pygame.Vector2(pos)
        self.attack_range = attack_range

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float, target: Player | None = None) -> None:
        anim = EnemyAnim.RUN
        to_target = pygame.Vector2()

        if target is not None:
            to_target = pygame.Vector2(target.rect.center) - self.pos
            if to_target.length() > self.attack_range:
                self.pos += to_target.normalize() * self.speed * dt
            else:
                anim = EnemyAnim.ATTACK

        if anim != self.current_anim:
            self.animations[anim].reset()
            self.current_anim = anim

        if target is not None and to_target.length_squared() > 0:
            if abs(to_target.x) > abs(to_target.y) * 1.5:
                direction = Direction.RIGHT if to_target.x >= 0 else Direction.LEFT
            elif abs(to_target.y) > abs(to_target.x) * 1.5:
                direction = Direction.DOWN if to_target.y >= 0 else Direction.UP
            else:
                direction = None
            if direction is not None:
                self.animations[self.current_anim].set_direction(direction.value)

        frame = self.animations[self.current_anim].update(dt)

        if frame is not None:
            self.image = frame
            self.rect = self.image.get_rect(center=self.pos)
            self.mask = pygame.mask.from_surface(self.image)
