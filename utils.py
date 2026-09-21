import random

import pygame


def get_movement_direction(keys: pygame.key.ScancodeWrapper) -> pygame.Vector2:
    move = pygame.Vector2()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        move.y -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        move.y += 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        move.x -= 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        move.x += 1

    if move.length_squared() > 0:
        move.normalize_ip()

    return move


def aim_direction(
    from_pos: pygame.Vector2, to_pos: pygame.Vector2
) -> pygame.Vector2:
    to_target = to_pos - from_pos
    if to_target.length_squared():
        return to_target.normalize()
    return pygame.Vector2(1, 0)


def direction_to_angle(direction: pygame.Vector2) -> float:
    return -direction.as_polar()[1]


DEFAULT_DIRECTIONS = ("up", "left", "down", "right")


def load_sprite_frames(
    sprite_sheet: pygame.Surface,
    frame_width: int,
    frame_height: int,
    *,
    frame_count: int | None = None,
    rows: int = 1,
    row_names=None,
    scale: int = 2,
    origin: tuple[int, int] = (0, 0),
) -> dict[str, list[pygame.Surface]]:
    sheet_w, sheet_h = sprite_sheet.get_size()
    ox, oy = origin

    if frame_count is None:
        frame_count = (sheet_w - ox) // frame_width

    if row_names is None:
        row_names = DEFAULT_DIRECTIONS[:rows]

    row_names = list(row_names)
    if len(row_names) != rows:
        raise ValueError(f"row_names ({len(row_names)}) != rows ({rows})")

    needed_w = ox + frame_count * frame_width
    needed_h = oy + rows * frame_height

    if sheet_w < needed_w or sheet_h < needed_h:
        raise ValueError(
            f"Лист {sheet_w}x{sheet_h}px не вмещает сетку: "
            f"нужно минимум {needed_w}x{needed_h}px "
            f"({frame_count} кадров по {frame_width}px, "
            f"{rows} рядов по {frame_height}px)"
        )

    out_w, out_h = frame_width * scale, frame_height * scale
    result: dict[str, list[pygame.Surface]] = {}

    for row, name in enumerate(row_names):
        row_frames = []
        for col in range(frame_count):
            rect = pygame.Rect(
                ox + col * frame_width,
                oy + row * frame_height,
                frame_width,
                frame_height,
            )
            frame = sprite_sheet.subsurface(rect)
            row_frames.append(pygame.transform.scale(frame, (out_w, out_h)))
        result[name] = row_frames

    return result


def tile_background(
    land_images: list[pygame.Surface], width: int, height: int
) -> pygame.Surface:
    bg_surface = pygame.Surface((width, height))
    tile_w = land_images[0].get_width()
    tile_h = land_images[0].get_height()

    for y in range(0, height, tile_h):
        for x in range(0, width, tile_w):
            cur_image = random.choice(land_images)
            bg_surface.blit(cur_image, (x, y))

    return bg_surface
