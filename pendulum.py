import pygame
import math

pygame.init()

WIDTH, HEIGHT = 2000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wahadło matematyczne")

fps = 60
timer = pygame.time.Clock()

BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
PURPLE = (139, 69, 199)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

running = True

alfa0 = math.pi / 4
alfa = 0
L = HEIGHT / 2

G = 9.81 

omega = math.sqrt(G / L)
time = 0
dt = 0.1

BEGINNING_X = WIDTH / 2

while running:
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BLACK)

    alfa = alfa0 * math.cos(omega * time)      
    x = L * math.sin(alfa)
    y = L * math.cos(alfa) 

    pygame.draw.line(screen, RED, (BEGINNING_X, 0), (BEGINNING_X + x, y), 5)

    pygame.draw.circle(screen, RED, (BEGINNING_X + x, y), 25)       

    pygame.display.flip()
    time += dt

pygame.quit()

