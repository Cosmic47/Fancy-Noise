import pygame
import sys
import random
import math


scr_w, scr_h = 1920, 1080  # Window simensions (Default 1920, 1080)
px_size = 8  # Pixels' side length (Default: 8)
color_threshold = 0.22  # Cells are similar if the difference of their values is less than this (Default: 0.22)
draw_threshold = 0.025  # Do not redraw the cell if it changed less by this value (Default: 0.025)

color_a = 200, 0, 0  # Unused
color_b = 0, 0, 0

width_in_px = int(math.ceil(scr_w / px_size))
height_in_px = int(math.ceil(scr_h / px_size))

def neighbour_idxs(y, x):
    # Neighbours are cells that share one side with the specified cell
    neighs = []
    if y > 0:
        neighs.append((y - 1, x))
    if y < height_in_px - 1:
        neighs.append((y + 1, x))
        
    if x > 0:
        neighs.append((y, x - 1))
    if x < width_in_px - 1:
        neighs.append((y, x + 1))

    """
    if x > 1:
        neighs.append((y, x - 2))
    if x < width_in_px - 2:
        neighs.append((y, x + 2))
    """

    return neighs

def float_to_color(t):
    # Convert a cell's value to a color
    """
    t = t**2 if t < 0.5 else 1 - t**2
    return [color_a[i] * (1 - t) + color_b[i] * t for i in (0,1,2)]
    """
    t = t**2 if t < 0.5 else 1 - t**2
    if t > 0.72:
        return 0, 255, 0
    elif t > 0.6:
        return 0, 200 * t, 230 * t
    else:
        return 0, 0, 150 * t
    """
    t = t**2 if t < 0.5 else 1 - t**2
    if t > 0.7:
        return 100, 255, 0
    elif t > 0.6:
        return 255, 230, 0
    else:
        return 60 * t, 60 * t, 60 * t
    """
    """
    palette = [(10*t, 10*t, 10*t) for t in range(26)]
    idx = int(round(t * (len(palette) - 1)))
    return palette[idx]
    """

def merge(pixels, updated, y, x):
    cur_color = pixels[y][x]
    avg_color = cur_color
    to_merge = set()

    # Get neighbours that are similar to the main pixel
    for ny, nx in neighbour_idxs(y, x):
        neigh_color = pixels[ny][nx]
        if abs(cur_color - neigh_color) <= color_threshold:
            avg_color += neigh_color
            to_merge.add((ny, nx))

    # If none such found, dont do anything
    if not to_merge:
        return

    # Color them average
    to_merge.add((y, x))
    avg_color /= len(to_merge)
    for ny, nx in to_merge:
        if abs(pixels[ny][nx] - avg_color) >= draw_threshold:
            updated.add((ny, nx))
        pixels[ny][nx] = avg_color

def draw_pixel(surf, pixels, y, x):
    color = float_to_color(pixels[y][x])
    pygame.draw.rect(surf, color, (x * px_size, y * px_size, px_size, px_size))

def main():
    # Init stuff
    pygame.init()
    screen = pygame.display.set_mode((scr_w, scr_h))
    clock = pygame.time.Clock()

    # Create noise
    arr = [[random.random() for x in range(width_in_px)] for y in range(height_in_px)]
    updated = set()
    for y in range(height_in_px):
        for x in range(width_in_px):
            draw_pixel(screen, arr, y, x)

    while True:
        # Handle window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Register updated cells
        updated = set()
        for y in range(height_in_px):
            for x in range(width_in_px):
                merge(arr, updated, y, x)

        # Draw updated cells
        for pos in updated:
            y, x = pos
            draw_pixel(screen, arr, y, x)

        pygame.display.update()
        clock.tick(60)

main()
