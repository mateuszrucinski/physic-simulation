import pygame
import math

pygame.init()

WIDTH, HEIGHT = 2000, 1000
SCALE_OF_PIXELS = 0.01
G = 9.81     

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wahadło matematyczne")

fps = 60
timer = pygame.time.Clock()

GREEN = (34, 139, 34)
BLUE = (0, 150, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

alfa0 = math.pi / 4  
L_pixels = HEIGHT / 2
L = L_pixels * SCALE_OF_PIXELS            
omega = math.sqrt(G / L)
time = 0
dt = 1 / fps
running_simulation = False
mass = 50
velocity = 0    

BEGINNING_X = WIDTH // 2
BEGINNING_Y = 100

# Przyciski start/stop
start_button = pygame.Rect(50, 50, 150, 50)
stop_button = pygame.Rect(250, 50, 150, 50)

# Suwaki do zmiany parametrów
angle_slider = pygame.Rect(50, 150, 300, 10)
length_slider = pygame.Rect(50, 250, 300, 10)
mass_slider = pygame.Rect(50, 350, 300, 10)

angle_value = 50  
length_value = 50  
mass_value = 50  

def calculate_physics():
    global velocity
    alfa = alfa0 * math.cos(omega * time)
    velocity = L * omega * math.sin(omega * time)  
    kinetic_energy = 0.5 * mass * velocity**2  
    potential_energy = mass * G * (L - L * math.cos(alfa))

    return velocity, kinetic_energy, potential_energy

def draw_pendulum():
    alfa = alfa0 * math.cos(omega * time)
    x = L_pixels * math.sin(alfa)
    y = L_pixels * math.cos(alfa)

    color_intensity = 255 - int((mass_value / 100) * 200)
    pendulum_color = (color_intensity, 0, 0)

    pygame.draw.line(screen, RED, (BEGINNING_X, BEGINNING_Y), (BEGINNING_X + x, BEGINNING_Y + y), 5)
    pygame.draw.circle(screen, pendulum_color, (int(BEGINNING_X + x), int(BEGINNING_Y + y)), 25)

VELOCITY_SCALE = 10

show_velocity_vector = True
show_gravitation_force_vector = True
checkbox_rect_v = pygame.Rect(50, 650, 30, 30)
checkbox_rect_fg = pygame.Rect(50, 700, 30, 30)

def draw_gravitation_force_vector(mass):
    alfa = alfa0 * math.cos(omega * time)
    x = L_pixels * math.sin(alfa)
    y = L_pixels * math.cos(alfa)

    Fg = mass * G

    scaled_Fg = Fg / 3

    pygame.draw.line(screen, GREEN, (BEGINNING_X + x, BEGINNING_Y + y), 
                     (BEGINNING_X + x, BEGINNING_Y + y + scaled_Fg), 3)
    


def draw_velocity_vector(velocity, alfa0):
    alfa = alfa0 * math.cos(omega * time)
    x = L_pixels * math.sin(alfa)
    y = L_pixels * math.cos(alfa)

    vx = -velocity * math.cos(alfa)
    vy = velocity * math.sin(alfa)

    vx_scaled = vx * VELOCITY_SCALE
    vy_scaled = vy * VELOCITY_SCALE

    pygame.draw.line(screen, BLUE, (BEGINNING_X + x, BEGINNING_Y + y), 
                     (BEGINNING_X + x + vx_scaled, BEGINNING_Y + y + vy_scaled), 3)

def draw_ui():
    velocity, kinetic_energy, potential_energy = calculate_physics()
    T = 2 * math.pi * math.sqrt(L / G)

    font = pygame.font.SysFont(None, 40)

    #start
    pygame.draw.rect(screen, GREEN if not running_simulation else GRAY, start_button)
    screen.blit(font.render("START", True, WHITE), (75, 60))

    #stop
    pygame.draw.rect(screen, RED if running_simulation else GRAY, stop_button)
    screen.blit(font.render("STOP", True, WHITE), (285, 60))

    #suwak kata
    pygame.draw.rect(screen, WHITE, angle_slider)
    pygame.draw.circle(screen, RED, (50 + int(3 * angle_value), 155), 15)
    screen.blit(font.render(f"Kąt: {round(angle_value / 100 * 90)}°", True, WHITE), (400, 140))

    #suwak dlugosci
    pygame.draw.rect(screen, WHITE, length_slider)
    pygame.draw.circle(screen, RED, (50 + int(3 * length_value), 255), 15)
    screen.blit(font.render(f"Długość: {round(L, 2)} m", True, WHITE), (400, 240))

    #suwak masy
    pygame.draw.rect(screen, WHITE, mass_slider)
    pygame.draw.circle(screen, RED, (50 + int(3 * mass_value), 355), 15)
    screen.blit(font.render(f"Masa: {round(mass_value / 100 * 100)} kg", True, WHITE), (400, 340))

    #wypisanie parametrow fizycznych
    screen.blit(font.render(f"Okres T: {T:.2f} s", True, WHITE), (50, 450))
    screen.blit(font.render(f"Prędkość V(t): {velocity:.2f} m/s", True, WHITE), (50, 500))
    screen.blit(font.render(f"Energia kinetyczna: {kinetic_energy:.2f} J", True, WHITE), (50, 550))
    screen.blit(font.render(f"Energia potencjalna: {potential_energy:.2f} J", True, WHITE), (50, 600))

    #checkboxy
    pygame.draw.rect(screen, WHITE, checkbox_rect_v, 2)
    if show_velocity_vector:
        pygame.draw.line(screen, WHITE, (checkbox_rect_v.left + 5, checkbox_rect_v.centery), 
                         (checkbox_rect_v.left + 12, checkbox_rect_v.bottom - 5), 3)
        pygame.draw.line(screen, WHITE, (checkbox_rect_v.left + 12, checkbox_rect_v.bottom - 5), 
                         (checkbox_rect_v.right - 5, checkbox_rect_v.top + 5), 3)
    screen.blit(font.render("Pokaż wektor prędkości", True, WHITE), (90, 650))

    pygame.draw.rect(screen, WHITE, checkbox_rect_fg, 2)
    if show_gravitation_force_vector:
        pygame.draw.line(screen, WHITE, (checkbox_rect_fg.left + 5, checkbox_rect_fg.centery), 
                         (checkbox_rect_fg.left + 12, checkbox_rect_fg.bottom - 5), 3)
        pygame.draw.line(screen, WHITE, (checkbox_rect_fg.left + 12, checkbox_rect_fg.bottom - 5), 
                         (checkbox_rect_fg.right - 5, checkbox_rect_fg.top + 5), 3)
    screen.blit(font.render("Pokaż wektor siły grawitacyjnej", True, WHITE), (90, 700))

running = True

while running:
    timer.tick(fps)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                running_simulation = True
            if stop_button.collidepoint(event.pos):
                running_simulation = False

            if checkbox_rect_v.collidepoint(event.pos):
                show_velocity_vector = not show_velocity_vector
            elif checkbox_rect_fg.collidepoint(event.pos):
                show_gravitation_force_vector = not show_gravitation_force_vector

            if angle_slider.collidepoint(event.pos):
                angle_value = max(0, min(100, (event.pos[0] - 50) // 3))
                alfa0 = (angle_value / 100) * (math.pi / 2)
            if length_slider.collidepoint(event.pos):
                length_value = max(0, min(100, (event.pos[0] - 50) // 3))
                L_pixels = (length_value / 100) * (HEIGHT / 2)
                L = L_pixels * SCALE_OF_PIXELS
                omega = math.sqrt(G / L)
            if mass_slider.collidepoint(event.pos):
                mass_value = max(0, min(100, (event.pos[0] - 50) // 3))
                mass = (mass_value / 100) * 100

    draw_pendulum()
    if(show_gravitation_force_vector):
        draw_gravitation_force_vector(mass)
    if show_velocity_vector:
        draw_velocity_vector(velocity, alfa0)
    draw_ui()

    if running_simulation:
        time += dt
    pygame.display.flip()

pygame.quit()
