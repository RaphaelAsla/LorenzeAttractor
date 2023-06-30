#!/usr/bin/env python3

import pygame

scale = 14

white = (255, 255, 255)
black = (0, 0, 0)

sigma = 10.0
beta = 8.0/3.0
rho = 28.0

dt = 0.01

def update_lorenz(x, y, z, sigma, beta, rho, dt):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    x += dx * dt
    y += dy * dt
    z += dz * dt
    return x, y, z

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.pos_history = []

diff = 0.000001
points = [Point(i*diff, i*diff, i*diff) for i in range(1, 1000)]

pygame.init()
screen = pygame.display.set_mode((1910, 1070))
pygame.display.set_caption('Lorenz System')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(black)

    for point in points:
        x = int(point.x * scale * 2) + 900
        y = int(point.z * scale) + 200

        if 0 <= x < 1910 and 0 <= y < 1070:
            point.pos_history.append([(x, y), point.y * scale])

            for i in range(1, len(point.pos_history)-1):
                prev_pos = point.pos_history[i][0]
                curr_pos = point.pos_history[i-1][0]
                color_diff = (abs(prev_pos[0] - curr_pos[0]) + abs(prev_pos[1] - curr_pos[1]) + abs(point.pos_history[i-1][1] - point.pos_history[i][1])) * 3
                color = (min(255, color_diff), 200, max(0, 255 - color_diff))
                pygame.draw.line(screen, color, prev_pos, curr_pos, 1)

            point.x, point.y, point.z = update_lorenz(point.x, point.y, point.z, sigma, beta, rho, dt)

        while len(point.pos_history) > 4:
            point.pos_history.pop(0)
    
    pygame.display.flip()

pygame.quit()
