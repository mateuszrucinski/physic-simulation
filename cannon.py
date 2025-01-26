import pygame
import math

pygame.init()

WIDTH, HEIGHT = 2800, 1400
SCALE_OF_PIXELS = 0.01
OY = HEIGHT - 250

G = 9.81   

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Armata")

fps = 60
timer = pygame.time.Clock()

time = 0
dt = 1 / fps

GREEN = (34, 139, 34)
BLUE = (0, 150, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
ORANGE = (255, 180, 80)

alfa = math.radians(45)

#armata
cannon_base = (100, OY)
cannon_radius = 50
cannon_barrel_width = 100
cannon_barrel_height = 100

#przyciski start, stop, restart
button_width, button_height = 150, 50
start_button = pygame.Rect(WIDTH // 2 - button_width // 2 - 200, HEIGHT - 80, button_width, button_height)
stop_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 80, button_width, button_height)
restart_button = pygame.Rect(WIDTH // 2 - button_width // 2 + 200, HEIGHT - 80, button_width, button_height)

#pole ladowania
target_position = [WIDTH - 400, OY - 15]
target_size = (200, 120)

dragging_target = False
dragging_cannon = False

class Bullet:
    def __init__(self, color, circle_positions, mass):
        self.color = color
        self.circle_positions = circle_positions
        self.mass = mass
        self.mass = mass

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.circle_positions, 30)

    def move(self, dx, dy):
        self.circle_positions[0] += dx
        self.circle_positions[1] -= dy

running = True
running_simulation = False
bullet_visible = False
hit_target = False

bullet = Bullet(color= BLACK, circle_positions= [100, OY - 1], mass= 100)

Vo = 15

mass_value = 50  
velocity_value = 50  


def draw_cannon():
    end_x = cannon_base[0] + cannon_barrel_height * math.cos(alfa)
    end_y = cannon_base[1] - cannon_barrel_height * math.sin(alfa)

    dx = (cannon_barrel_width / 2) * math.sin(alfa)
    dy = (cannon_barrel_width / 2) * math.cos(alfa)

    #lufa
    barrel_points = [
        (cannon_base[0] - dx, cannon_base[1] - dy),
        (cannon_base[0] + dx, cannon_base[1] + dy), 
        (end_x + dx, end_y + dy),  
        (end_x - dx, end_y - dy)
    ]
    pygame.draw.polygon(screen, RED, barrel_points)

    #kolko armaty
    pygame.draw.circle(screen, RED, cannon_base, cannon_radius)

    #krzyzyk
    pygame.draw.line(screen, BLACK, (cannon_base[0] - 15, cannon_base[1]), (cannon_base[0] + 15, cannon_base[1]), 5)
    pygame.draw.line(screen, BLACK, (cannon_base[0], cannon_base[1] - 15), (cannon_base[0], cannon_base[1] + 15), 5)

def draw_target():
    pygame.draw.rect(screen, YELLOW, (*target_position, *target_size))

def draw_buttons():
    pygame.draw.rect(screen, ORANGE, start_button)
    pygame.draw.rect(screen, ORANGE, stop_button)
    pygame.draw.rect(screen, ORANGE, restart_button)

    font = pygame.font.Font(None, 40)
    screen.blit(font.render("START", True, BLACK), (start_button.x + 40, start_button.y + 10))
    screen.blit(font.render("STOP", True, BLACK), (stop_button.x + 50, stop_button.y + 10))
    screen.blit(font.render("RESTART", True, BLACK), (restart_button.x + 25, restart_button.y + 10))

def reset_simulation():
    global bullet, time, running_simulation, bullet_visible, alfa

    bullet.circle_positions = [100, OY - 1]
    
    time = 0
    running_simulation = False
    bullet_visible = False

def calculate_physics():
    velocity_x = Vo * math.cos(alfa)
    velocity_y = Vo * math.sin(alfa) - G * time
    velocity = math.sqrt(velocity_x**2 + velocity_y**2)
    kinetic_energy = 0.5 * bullet.mass * velocity**2
    potential_energy = bullet.mass * G * (OY - bullet.circle_positions[1])
    distance_to_target_X = (target_position[0] + target_size[0] / 2) - cannon_base[0] 

    return velocity, kinetic_energy, potential_energy, distance_to_target_X

# suwaki do zmiany parametrów
mass_slider = pygame.Rect(WIDTH - 450, 150, 300, 10)
velocity_slider = pygame.Rect(WIDTH - 450, 250, 300, 10)
angle_slider = pygame.Rect(WIDTH - 450, 350, 300, 10)

def draw_ui():
    velocity, kinetic_energy, potential_energy, distance_to_target_X = calculate_physics()
    font = pygame.font.SysFont(None, 40)

    pygame.draw.rect(screen, WHITE, mass_slider)
    pygame.draw.circle(screen, RED, (mass_slider.x + int(3 * mass_value), mass_slider.y + 5), 15)
    screen.blit(font.render(f"Masa: {round(mass_value)} kg", True, WHITE), (WIDTH - 420, 120))

    pygame.draw.rect(screen, WHITE, velocity_slider)
    pygame.draw.circle(screen, RED, (velocity_slider.x + int(3 * velocity_value), velocity_slider.y + 5), 15)
    screen.blit(font.render(f"Prędkość: {round(velocity_value)} m/s", True, WHITE), (WIDTH - 420, 220))

    pygame.draw.rect(screen, WHITE, angle_slider)
    pygame.draw.circle(screen, RED, (angle_slider.x + int(3 * math.degrees(alfa)), angle_slider.y + 5), 15)
    screen.blit(font.render(f"Kąt: {round(math.degrees(alfa))}°", True, WHITE), (WIDTH - 420, 320))

    screen.blit(font.render(f"Prędkość: {velocity:.2f} m/s", True, WHITE), (WIDTH - 450, 450))
    screen.blit(font.render(f"Energia kinetyczna: {kinetic_energy:.2f} J", True, WHITE), (WIDTH - 450, 500))
    screen.blit(font.render(f"Energia potencjalna: {potential_energy:.2f} J", True, WHITE), (WIDTH - 450, 550))

    screen.blit(font.render(f"Odległosc od armaty: {(distance_to_target_X * SCALE_OF_PIXELS):.2f} m", True, YELLOW), (WIDTH - 450, 650))

def check_collision():
    global hit_target, running_simulation
    bullet_x, bullet_y = bullet.circle_positions

    if target_position[0] <= bullet_x <= target_position[0] + target_size[0] and bullet_y >= target_position[1]:
        hit_target = True

while running:
    timer.tick(fps)
    screen.fill(BLUE)

    pygame.draw.rect(screen, GREEN, (0, OY, WIDTH, 250))

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos) and bullet.circle_positions[1] < OY:
                running_simulation = True
            elif stop_button.collidepoint(event.pos):
                running_simulation = False
            elif restart_button.collidepoint(event.pos):
                running_simulation = False
                reset_simulation() 

            if mass_slider.collidepoint(event.pos):
                mass_value = max(1, min(100, (event.pos[0] - mass_slider.x) // 3))
                bullet.mass = mass_value
            if velocity_slider.collidepoint(event.pos):
                velocity_value = max(1, min(100, (event.pos[0] - velocity_slider.x) // 3))
                Vo = velocity_value
            if angle_slider.collidepoint(event.pos):
                angle_value = max(0, min(90, (event.pos[0] - angle_slider.x) // 3))
                alfa = math.radians(angle_value)

            if pygame.Rect(*target_position, *target_size).collidepoint(event.pos):
                dragging_target = True
            
            end_x = cannon_base[0] + cannon_barrel_height * math.cos(alfa)
            end_y = cannon_base[1] - cannon_barrel_height * math.sin(alfa)

            dx = (cannon_barrel_width / 2) * math.cos(alfa)
            dy = (cannon_barrel_width / 2) * math.sin(alfa)

            #lufa
            barrel_points = [
                (cannon_base[0] - dx, cannon_base[1] - dy),
                (cannon_base[0] + dx, cannon_base[1] + dy), 
                (end_x + dx, end_y + dy),  
                (end_x - dx, end_y - dy)
            ]
            if pygame.draw.polygon(screen, RED, barrel_points).collidepoint(event.pos):
                dragging_cannon = True

        if event.type == pygame.MOUSEBUTTONUP:
            dragging_target = False
            dragging_cannon = False
 

        #przeciąganie pola lądowania 
        if event.type == pygame.MOUSEMOTION and dragging_target:
            new_x = event.pos[0] - target_size[0] // 2  # Ustawienie pozycji na środku kursora
            # ograniczenie zakresu przesuwania w poziomie
            if 0 <= new_x <= WIDTH - target_size[0]:
                target_position[0] = new_x

        #zmiana kata lufy armaty
        if event.type == pygame.MOUSEMOTION and dragging_cannon:
            dx = event.pos[0] - cannon_base[0]
            dy = cannon_base[1] - cannon_radius - event.pos[1]
            angle = math.atan2(dy, dx)
            if 0 <= angle <= math.pi / 2:
                alfa = angle

    draw_cannon()
    draw_target()
    draw_buttons()
    draw_ui()

    if bullet_visible:
        bullet.draw(screen)

    if running_simulation:
        bullet_visible = True
        if bullet.circle_positions[1] >= OY:
            running_simulation = False
            check_collision()
        dx = Vo * math.cos(alfa) * time
        dy = Vo * math.sin(alfa) * time - ((G * time**2) / 2)

        bullet.move(dx, dy)
        # bullet.draw(screen)

        time += dt

    if hit_target:
                font = pygame.font.Font(None, 100)
                text = font.render("Brawo!!!:)", True, WHITE)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
