import pygame
import math

pygame.init()

# Ustawienia ekranu
WIDTH, HEIGHT = 2800, 1400
SCALE_OF_PIXELS = 0.01
OY = HEIGHT - 250

G = 5  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Armata")

fps = 60
timer = pygame.time.Clock()

time = 0
dt = 1 / fps

# Kolory
GREEN = (124,252,0)
BLUE = (0, 150, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
ORANGE = (255, 180, 80)
PURPLE = (148,0,211)

# Przycisk start, stop, restart
button_width, button_height = 150, 50
start_button = pygame.Rect(WIDTH // 2 - button_width // 2 - 200, OY + 125, button_width, button_height)
# stop_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 80, button_width, button_height)
# restart_button = pygame.Rect(WIDTH // 2 - button_width // 2 + 200, HEIGHT - 80, button_width, button_height)

def draw_buttons():
    """Rysowanie przycisków"""
    pygame.draw.rect(screen, ORANGE, start_button)
    # pygame.draw.rect(screen, ORANGE, stop_button)
    # pygame.draw.rect(screen, ORANGE, restart_button)

    font = pygame.font.Font(None, 40)
    screen.blit(font.render("START", True, BLACK), (start_button.x + 40, start_button.y + 10))
    # screen.blit(font.render("STOP", True, BLACK), (stop_button.x + 50, stop_button.y + 10))
    # screen.blit(font.render("RESTART", True, BLACK), (restart_button.x + 25, restart_button.y + 10))

class Planet:
    def __init__(self, color, radius, planet_position, velocity_end_point, Vx, Vy, is_planet_settled, is_velocity_settled, mass):
        self.color = color
        self.radius = radius
        self.planet_position = list(planet_position)
        self.velocity_end_point = list(velocity_end_point) 
        self.Vx = Vx
        self.Vy = Vy
        self.is_planet_settled = is_planet_settled
        self.is_velocity_settled = is_velocity_settled
        self.mass = mass

    def collidepoint(self, point):
        distance = math.sqrt((self.planet_position[0] - point[0])**2 + (self.planet_position[1] - point[1])**2)
        return distance <= self.radius
    
    def collidepoint_velocity_end_point(self, point):
        distance = math.sqrt((self.velocity_end_point[0] - point[0])**2 + (self.velocity_end_point[1] - point[1])**2)
        return distance <= 20
    
    def countVx(self):
        self.Vx =  self.velocity_end_point[0] - self.planet_position[0]

    def countVy(self):
        self.Vy = self.velocity_end_point[1] - self.planet_position[1]

    def count_velocity_value(self):
        self.velocity_value = math.sqrt((self.velocity_end_point[0] - self.planet_position[0])**2 + (self.velocity_end_point[1] - self.planet_position[1])**2)

    def move(self, dx, dy):
        self.planet_position[0] += dx
        self.planet_position[1] -= dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.planet_position, self.radius)
        
        #wektor predkosci
        pygame.draw.line(screen, WHITE, self.planet_position, self.velocity_end_point, 2)
        

    # def move(self, dx, dy):
    #     self.circle_positions[0] += dx
    #     self.circle_positions[1] -= dy

planeta1 = Planet(RED, 30, [50, OY + 125], [50, OY + 125], 0, 0, False, False, 50)
planeta2 = Planet(GREEN, 50, [200, OY + 125], [200, OY + 125], 0, 0, False, False, 80)
planeta3 = Planet(PURPLE, 80, [400, OY + 125], [400, OY + 125], 0, 0, False, False, 100)

planets_to_choose = [planeta1, planeta2, planeta3]

planets_in_simulation = []
dragging = None

# is_planet_settled = False
# is_velocity_settled = False

velocity_dragging = False
planet_dragging = False

running = True
running_simulation = False

while running:
    timer.tick(fps)
    screen.fill(BLACK)

    # Rysowanie podłoża
    pygame.draw.rect(screen, (47,79,79), (0, OY, WIDTH // 5, 250))

    for planeta in planets_to_choose:
        planeta.draw(screen)
    
    draw_buttons()

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for planeta in planets_to_choose:
                if planeta.collidepoint(event.pos):
                    velocity_dragging = False
                    planet_dragging = False
                    
                    newPlanet = Planet(planeta.color, planeta.radius, planeta.planet_position, planeta.velocity_end_point, 0, 0, False, False, planeta.mass)
                    dragging = newPlanet
                    planets_in_simulation.append(dragging)
                    planet_dragging = True
            
            for obj in planets_in_simulation:
                if obj.collidepoint(event.pos):
                    dragging = obj
                    if dragging.is_planet_settled == True:
                        if not dragging.is_velocity_settled:
                            velocity_dragging = True
                        else:
                            planet_dragging = True
                        break
                if obj.collidepoint_velocity_end_point(event.pos):
                    dragging = obj
                    if dragging.is_velocity_settled:
                        velocity_dragging = True
                    break
            
            if start_button.collidepoint(event.pos):
                planets_in_simulation[1].countVx()
                planets_in_simulation[1].countVy()
                running_simulation = True
                        
        if event.type == pygame.MOUSEBUTTONUP:
            if planet_dragging:
                if dragging.is_planet_settled == False:
                    dragging.is_planet_settled = True
                planet_dragging = False
                dragging = None
            elif velocity_dragging:
                if dragging.is_velocity_settled == False:
                    dragging.is_velocity_settled = True
                velocity_dragging = False
                dragging = None

        if event.type == pygame.MOUSEMOTION:
            if planet_dragging:
                if dragging.is_planet_settled:
                    dragging.planet_position = list(event.pos)
                else:    
                    dragging.planet_position = list(event.pos)
                    dragging.velocity_end_point = list(event.pos)
            elif velocity_dragging:
                dragging.velocity_end_point = list(event.pos)

    for planeta in planets_in_simulation:
        planeta.draw(screen)

    if running_simulation:
        #wyznaczenie odleglosci
            rx = planets_in_simulation[0].planet_position[0] - planets_in_simulation[1].planet_position[0] 
            ry = planets_in_simulation[0].planet_position[1] - planets_in_simulation[1].planet_position[1] 
            r = math.sqrt(rx**2 + ry**2)

            alfa = math.atan2(ry, rx)

            Fg = (G * planets_in_simulation[0].mass * planets_in_simulation[1].mass) / (r**2)

            Fgx = Fg * math.cos(alfa)
            Fgy = Fg * math.sin(alfa)

            planet1 = planets_in_simulation[1]

            planet1.Vx += Fgx / planet1.mass * time 
            planet1.Vy += Fgy / planet1.mass * time

            dx = planet1.Vx * time
            dy = planet1.Vy * time

            planet1.move(dx, dy)


            time += dt 
        # for planeta in planets_in_simulation:
            #wyselekcjonowanie planet które maja predkosci rozne od zera
            # if planeta.velosity_value > 0:

            #wyznaczenie odleglosci
            # rx = planeta 
            # r = 
            
    pygame.display.flip()

pygame.quit()
