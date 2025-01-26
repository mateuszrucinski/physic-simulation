import pygame

pygame.init()

WIDTH, HEIGHT = 2000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Przeciąganie skrzyni")

font = pygame.font.Font(None, 36)

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
WHITE = (255, 255, 255)

x0 = WIDTH // 2


resultat_force = 0
resultat_red_force = 0
resultat_blue_force = 0
total_mass = 0
resultat_velocity = 0
acceleration = 0

def set_resultat_force(force, color):
    global resultat_force
    global resultat_red_force
    global resultat_blue_force
    if (color == RED):
        resultat_red_force -= force
    elif (color == CYAN):
        resultat_blue_force += force
    resultat_force = resultat_blue_force + resultat_red_force

def draw_arrow(resultat_force, color):
    y_strongmen_resultat_force = 150 if (color != GREEN) else 200

    start_pos = (x0, y_strongmen_resultat_force)
    end_pos = (x0 + resultat_force, y_strongmen_resultat_force)

    if (resultat_force != 0):
        pygame.draw.line(screen, color, start_pos, end_pos, 15)

        arrow_size = 30 if resultat_force > 0 else -30
        end_pos_arrow = (end_pos[0] + 10, end_pos[1]) if resultat_force > 0 else (end_pos[0] - 10, end_pos[1])

        pygame.draw.polygon(screen, color, [
            end_pos_arrow, 
            (end_pos[0] - arrow_size, end_pos[1] - 30),
            (end_pos[0] - arrow_size, end_pos[1] + 30)
        ])


        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"{resultat_force}N", True, BLACK)
        text_rect = text_surface.get_rect(center=((start_pos[0] + end_pos[0]) // 2, start_pos[1] - 20))
        screen.blit(text_surface, text_rect)

class Strongman:
    def __init__(self, force, width, height, color, position, side, mass, is_in_game=False):
        self.force = force
        self.width = width
        self.height = height
        self.color = color
        self.original_pos = position
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.side = side
        self.mass = mass
        self.is_in_game = is_in_game
    
    def move(self, dx):
        if self.is_in_game:
            self.rect.x += dx
    
    def __repr__(self):
        return (f"Strongman(force={self.force}, width={self.width}, height={self.height}, "
                f"color={self.color}, position={self.original_pos}, side={self.side}, "
                f"mass={self.mass}, is_in_game={self.is_in_game})")

class Crate:
    def __init__(self, width, height, color, position, mass):
        self.width = width
        self.height = height
        self.color = color
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.mass = mass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move(self, dx):
        # print(f"Wartosc przed: {self.rect.x}")
        self.rect.x += dx
        # print(f"Wartosc po: {self.rect.x}")

class Rope:
    def __init__(self, color, circle_positions, rope_y, mass):
        self.color = color
        self.circle_positions = circle_positions
        self.rope_y = rope_y
        self.mass = mass

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (self.circle_positions[0][0], self.rope_y), (self.circle_positions[-1][0], self.rope_y), 5)
        for circle in self.circle_positions:
            pygame.draw.circle(screen, self.color, circle, 25)

    def move(self, dx):
        for i in range(len(self.circle_positions)):
            self.circle_positions[i] = (self.circle_positions[i][0] + dx, self.circle_positions[i][1])


rope_y = HEIGHT // 2 - 50
beggining_circle_positions = [(x, rope_y) for x in range(500, 1700, 200)]

RED_STRONGMAN_START_POSITION = 100

strongmen_list = [
    Strongman(150, 50, 150, RED, (RED_STRONGMAN_START_POSITION, HEIGHT - 400), "left", 130),
    Strongman(100, 50, 100, RED, (RED_STRONGMAN_START_POSITION + 100, HEIGHT - 350), "left", 100),
    Strongman(50, 50, 50, RED, (RED_STRONGMAN_START_POSITION + 200, HEIGHT - 300), "left", 80),
    Strongman(150, 50, 150, CYAN, (WIDTH - 200, HEIGHT - 400), "right", 130),
    Strongman(100, 50, 100, CYAN, (WIDTH - 300, HEIGHT - 350), "right", 100),
    Strongman(50, 50, 50, CYAN, (WIDTH - 400, HEIGHT - 300), "right", 80),
]

strongmen_list_in_game = []

crate = Crate(100, 100, PURPLE, (WIDTH // 2 - 50, rope_y - 50), 200)
rope = Rope(PURPLE, beggining_circle_positions, rope_y, 50)

start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 210, 100, 50)
stop_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 140, 100, 50)
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 50)

dragging = None
animation_active = False

is_strongmen_from_line = False

dt = 0.25

def draw_physics_parameters():
    simulation_time = pygame.time.get_ticks() / 1000  # Czas symulacji w sekundach

    position_text = f"Położenie x(t): {(crate.rect.x - 950):.2f} px"
    velocity_text = f"Prędkość V(t): {resultat_velocity:.2f} px/s"
    acceleration_text = f"Przyspieszenie a(t): {acceleration:.2f} px/s²"
    time_text = f"Czas symulacji: {simulation_time:.2f} s"

    screen.blit(font.render(position_text, True, WHITE), (WIDTH - 300, 50))
    screen.blit(font.render(velocity_text, True, WHITE), (WIDTH - 300, 100))
    screen.blit(font.render(acceleration_text, True, WHITE), (WIDTH - 300, 150))
    screen.blit(font.render(time_text, True, WHITE), (WIDTH - 300, 200))


def count_second_law_of_dynamics_parameters(force, color):
    global total_mass, acceleration
    strongmen_list_in_game_mass = sum(obj.mass for obj in strongmen_list_in_game)
    total_mass = strongmen_list_in_game_mass + crate.mass + rope.mass
    print(strongmen_list_in_game)
    set_resultat_force(force, color)
    print(f"resultat_force_red: {resultat_red_force}")
    print(f"resultat_force_blue: {resultat_blue_force}")
    print(f"resultat_force: {resultat_force}")

    print(f"mass of strongmens {strongmen_list_in_game_mass}")
    acceleration = resultat_force / total_mass if total_mass > 0 else 0
    print(f"acceleration {acceleration}")

def reset_simulation():
    global resultat_force, resultat_red_force, resultat_blue_force
    global total_mass, resultat_velocity, acceleration, strongmen_list_in_game, crate, rope

    resultat_force = 0
    resultat_red_force = 0
    resultat_blue_force = 0
    total_mass = 0
    resultat_velocity = 0
    acceleration = 0

    crate.rect.topleft = (WIDTH // 2 - 50, rope_y - 50)
    rope.circle_positions = [(x, rope_y) for x in range(500, 1700, 200)]

    strongmen_list_in_game.clear()

    for obj in strongmen_list:
        obj.rect.topleft = obj.original_pos

running = True
while running:
    timer.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                animation_active = True
                print(f"animation_active {animation_active}")
            elif stop_button.collidepoint(event.pos):
                animation_active = False
            elif restart_button.collidepoint(event.pos):
                animation_active = False
                reset_simulation() 
                print("Symulacja zresetowana.")
            for obj in strongmen_list:
                if obj.rect.collidepoint(event.pos):
                    dragging = Strongman(obj.force, obj.width, obj.height, obj.color, obj.original_pos, obj.side, obj.mass, True)
                    strongmen_list.append(dragging)
                    break
            for obj in strongmen_list_in_game:
                if obj.rect.collidepoint(event.pos):
                    dragging = obj
                    strongmen_list_in_game.remove(obj)
                    count_second_law_of_dynamics_parameters(-dragging.force, dragging.color)
                    break

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dropped = False
                left_circles = rope.circle_positions[:len(rope.circle_positions)//2]
                right_circles = rope.circle_positions[len(rope.circle_positions)//2:]

                valid_circles = left_circles if dragging.side == "left" else right_circles
                for circle in valid_circles:
                    circle_rect = pygame.Rect(circle[0] - 25, circle[1] - 25, 50, 50)
                    if circle_rect.collidepoint(event.pos):
                        dragging.rect.center = circle
                        strongmen_list_in_game.append(dragging)
                        count_second_law_of_dynamics_parameters(dragging.force, dragging.color)        
                        dropped = True
                        break
                if not dropped:
                    strongmen_list.remove(dragging)
                    # if is_strongmen_from_line:
                dragging = None

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                dragging.rect.center = event.pos

    if animation_active:
        resultat_velocity = acceleration * dt + resultat_velocity
        print(f"velocity {resultat_velocity}")
        #pochodna drogi to predkosc
        dx = int(resultat_velocity * dt)
        crate.move(dx)
        rope.move(dx)
        for obj in strongmen_list_in_game:
            obj.move(dx)

    screen.fill(BLUE)
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - HEIGHT // 3, WIDTH, HEIGHT // 3))

    rope.draw(screen)
    crate.draw(screen)

    draw_arrow(resultat_red_force ,RED)
    draw_arrow(resultat_blue_force, CYAN)
    draw_arrow(resultat_force, GREEN) 

    draw_physics_parameters()

    pygame.draw.rect(screen, YELLOW, start_button)
    font = pygame.font.Font(None, 36)
    text = font.render("START", True, BLACK)
    screen.blit(text, (start_button.x + 10, start_button.y + 10))

    pygame.draw.rect(screen, YELLOW, stop_button)
    font = pygame.font.Font(None, 36)
    text = font.render("STOP", True, BLACK)
    screen.blit(text, (stop_button.x + 10, stop_button.y + 10))

    pygame.draw.rect(screen, YELLOW, restart_button)
    font = pygame.font.Font(None, 28)
    text = font.render("RESTART", True, BLACK)
    screen.blit(text, (restart_button.x + 10, restart_button.y + 10))

    for obj in strongmen_list:
        pygame.draw.rect(screen, obj.color, obj.rect)
        
    for obj in strongmen_list_in_game:
        pygame.draw.rect(screen, obj.color, obj.rect)

    pygame.display.flip()

pygame.quit()
