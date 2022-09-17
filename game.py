import pygame
import numpy as np
from material import Material
from generator import Generator
from decoration import DecorationType
from world import World

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 900
GAME_NAME = "Landscape Mosaic"
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60  # Game is locked at 30 FPS
map_width, map_height = 0, 0
tile_scale = 3  # How "Zoomed in" the map appears, bigger numbers = more zoomed in
camera_speed = 6
camera_pos = [0, 0]
font = pygame.font.SysFont("Arial", 32, bold=True)
clock = pygame.time.Clock()

world = World()

""" Called only one time

 Does everything that needs to be done in terms of initializing the game
"""


def start_game(config_data, tile_map_input=None):
    Material.convert_images()
    DecorationType.convert_images()
    global map_width, map_height
    map_width = config_data["world"]["width"]
    map_height = config_data["world"]["width"]
    pygame.display.set_caption(GAME_NAME)
    if tile_map_input is None:
        generator = Generator(config_data)
        world.set_tile_map(generator.tile_map)
    else:
        world.set_tile_map(tile_map_input)
    size = len(world.tile_map)
    world_rects = np.empty((map_width, map_height), dtype="object")
    for row in range(size):
        for col in range(size):
            world_rects[row][col] = pygame.Rect(16*tile_scale*row, 16*tile_scale*col, 16*tile_scale, 16*tile_scale)
    game_loop()
    return world.tile_map


""" The Game Loop: runs the main loop that controls all the game logic

 Runs a certain number of times every second, ends when the window is closed
"""


def game_loop():
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                zoom_camera(event)

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                world_pos = ((pos[0] + camera_pos[0]) // (16*tile_scale), (pos[1] + camera_pos[1]) // (16*tile_scale))
                tile = world.tile_map[world_pos[1]][world_pos[0]]
                if event.button == 1:
                    tile.lower()
                if event.button == 3:
                    tile.increase()

        keys_pressed = pygame.key.get_pressed()
        move_camera(keys_pressed)

        for row in world.tile_map:
            for tile in row:
                if tile.decorations[0] is not None:
                    tile.decorations[0].update()
                if tile.decorations[1] is not None:
                    tile.decorations[1].update()

        draw()

    pygame.quit()


""" Controls the camera movement

 W = move up, A = move left, S = move down, D = move right
"""


def move_camera(keys_pressed):
    global camera_speed
    speed_increased = False
    if keys_pressed[pygame.K_LCTRL]:  # Holding left control doubles movement speed
        speed_increased = True
        camera_speed *= 2
    if keys_pressed[pygame.K_w]:  # Move Up
        camera_pos[1] -= camera_speed
        if camera_pos[1] < 0:
            camera_pos[1] = 0
#        for row in world_rects:
#            for rect in row:
#                rect.y += camera_speed
    if keys_pressed[pygame.K_a]:  # Move Left
        camera_pos[0] -= camera_speed
        if camera_pos[0] < 0:
            camera_pos[0] = 0
#        for row in world_rects:
#            for rect in row:
#                rect.x += camera_speed
    if keys_pressed[pygame.K_s]:  # Move Down
        camera_pos[1] += camera_speed
        if camera_pos[1] > map_height * tile_scale * 16 - WINDOW_HEIGHT:
            camera_pos[1] = map_height * tile_scale * 16 - WINDOW_HEIGHT
#        for row in world_rects:
#            for rect in row:
#                rect.y -= camera_speed
    if keys_pressed[pygame.K_d]:  # Move Right
        camera_pos[0] += camera_speed
        if camera_pos[0] > map_width * tile_scale * 16 - WINDOW_WIDTH:
            camera_pos[0] = map_width * tile_scale * 16 - WINDOW_WIDTH
#        for row in world_rects:
#            for rect in row:
#                rect.x -= camera_speed
    if speed_increased:
        camera_speed = camera_speed // 2


""" Controls the zooming of the mouse

 Controls are how the mouse scroll wheel is normally used
"""


def zoom_camera(event):
    global tile_scale
    if event.button == 4:  # Zoom in
        if tile_scale < 10:
            # Camera position must be modified relative to center point of current window
            # Otherwise it will zoom towards and away from the origin, which is unintuitive for users
            camera_pos[0] = ((camera_pos[0] + WINDOW_WIDTH // 2) // tile_scale) * (tile_scale + 1) - WINDOW_WIDTH // 2
            camera_pos[1] = ((camera_pos[1] + WINDOW_HEIGHT // 2) // tile_scale) * (tile_scale + 1) - WINDOW_HEIGHT // 2
            tile_scale += 1
    elif event.button == 5:  # Zoom out
        if tile_scale > 1:
            camera_pos[0] = ((camera_pos[0] + WINDOW_WIDTH // 2) // tile_scale) * (tile_scale - 1) - WINDOW_WIDTH // 2
            camera_pos[1] = ((camera_pos[1] + WINDOW_HEIGHT // 2) // tile_scale) * (tile_scale - 1) - WINDOW_HEIGHT // 2
            tile_scale -= 1

            # If you zoom out next to the edge of the map, the camera should be readjusted
            # Such that you cannot see outside of the map
            if camera_pos[0] < 0:
                camera_pos[0] = 0
            if camera_pos[1] < 0:
                camera_pos[1] = 0
            if camera_pos[0] > map_width * tile_scale * 16 - WINDOW_WIDTH:
                camera_pos[0] = map_width * tile_scale * 16 - WINDOW_WIDTH
            if camera_pos[1] > map_height * tile_scale * 16 - WINDOW_HEIGHT:
                camera_pos[1] = map_height * tile_scale * 16 - WINDOW_HEIGHT


""" This is run every frame, it renders everything on the screen

 Handles the logic for what is currently on the screen as well
"""


def draw():
    WIN.fill((0, 0, 0))
    tile_map = world.tile_map
    tile_size = tile_scale * 16
    startx, starty = camera_pos[0] // tile_size, camera_pos[1] // tile_size
    endx, endy = (camera_pos[0] + WINDOW_WIDTH) // tile_size + 2, \
                 (camera_pos[1] + WINDOW_HEIGHT) // tile_size + 2
    for y in range(starty, endy):
        for x in range(startx, endx):
            if x >= map_width or y >= map_height or x < 0 or y < 0:
                continue
            tile = tile_map[y][x]
            mat = tile.material
            dec1, dec2 = tile.decorations
            img1 = pygame.transform.scale(mat.img, (tile_size, tile_size))
            xdist, ydist = x*tile_size - camera_pos[0], y*tile_size - camera_pos[1]
            WIN.blit(img1, (xdist, ydist))
            if dec1 is not None:
                res = dec1.res
                fac = (16 - res) * tile_scale  # Decorations of different resolutions need different offset
                img2 = pygame.transform.scale(dec1.get_img(), (tile_scale*res, tile_scale*res))
                WIN.blit(img2, (xdist - tile_size / 2 + fac, ydist - tile_size / 2 + fac))
            if dec2 is not None:
                res = dec2.res
                fac = (16 - res) * tile_scale
                img2 = pygame.transform.scale(dec2.get_img(), (tile_scale * res, tile_scale * res))
                WIN.blit(img2, (xdist + fac, ydist + fac))
    WIN.blit(update_fps(), (20, 5))
    pygame.display.update()


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render("FPS : " + fps, True, pygame.Color("coral"))
    return fps_text

